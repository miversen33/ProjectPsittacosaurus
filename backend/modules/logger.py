import logging
from pathlib import Path
from logging import LogRecord, StreamHandler, Handler, FileHandler, Formatter
from datetime import datetime
import time
from threading import Thread
from collections import deque

from flask import current_app as app

try:
    with app.app_context():
        from models.log import Log
except:
    pass

def init_logger(app: app, logger_name='root'):
    formatter = Formatter('%(asctime)s %(name)s %(filename)s:%(lineno)d:%(levelname)s: %(message)s')
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(app.config.get('LOG_LEVEL', logging.INFO))
    [
        logger.addHandler(handler) for handler in 
        [_get_stream_handler(app, formatter), _get_file_handler(app, formatter),
         _get_db_handler(app)
         ]
    ]

def _get_file_handler(app: app, formatter: str):
    # Creates parent path
    log_location: Path = app.config.get('LOG_LOCATION')
    log_location.mkdir(parents=True, exist_ok=True)

    # Creates actual log path
    log_location = log_location / 'log'
    log_location.touch(exist_ok=True)

    file_handler = FileHandler(log_location.resolve())
    file_handler.setFormatter(formatter)
    file_handler.setLevel(app.config.get('LOG_LEVEL', logging.INFO))

    return file_handler
def _get_stream_handler(app: app, formatter: str):
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(app.config.get('LOG_LEVEL', logging.INFO))
    return stream_handler

def _get_db_handler(app: app):
    db_handler: _DB_Handler = None

    with app.app_context():
        db_handler = _DB_Handler(app)

    db_handler.setLevel(app.config.get('LOG_LEVEL', logging.INFO))
    return db_handler

class _DB_Handler(Handler):
    _TIMEOUT = 60
    _HOLDING_QUEUE_LIMIT = 100
    _inited = False

    def __init__(self, app, level=logging.NOTSET) -> None:
        super().__init__(level=level)
        self._app = app
        self._log_queue = deque([], _DB_Handler._HOLDING_QUEUE_LIMIT)
        Thread(target=self.__wait_for_db).start()

    def __wait_for_db(self):
        timeout = time.time() + _DB_Handler._TIMEOUT
        dun = False
        with self._app.app_context():
            while not dun and time.time() < timeout:
                time.sleep(.5)
                try:
                    dun = True if self._app.db.session.__dict__.get('attempt_commit') else False
                except:
                    dun = False
        if not dun:
            return
        from models.log import Log
        globals()['Log'] = Log
        self._inited = True
        self._process_logs()

    def emit(self, record: LogRecord) -> None:
        self._process_logs(record)

    def _process_logs(self, log: LogRecord=None) -> None:
        if not self._inited and log:
            self._log_queue.append(log)
            return

        for log in self._log_queue:
            self._save_log(log)
        self._log_queue.clear()
        if log:
            self._save_log(log)

    def _save_log(self, log: LogRecord) -> None:
        timestamp = log.asctime.split(',')[0].split(' ')
        year, month, day = timestamp[0].split('-')
        hour, minute, second = timestamp[1].split(':')
        d = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))
        new_log = Log(
            time=d,
            level=log.levelname,
            filename=log.filename,
            filepath=log.pathname,
            line_number=log.lineno,
            logger_name=log.name,
            message=log.message
        )
        with self._app.app_context():
            db = self._app.db
            db.session.add(new_log)
            db.session.attempt_commit()