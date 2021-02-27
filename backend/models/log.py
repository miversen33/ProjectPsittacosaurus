from flask import current_app as app
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .auth import User

class APILog(app.db.Model):
    __tablename__ = 'api_log'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False
    )

    user_id = Column(
        'user_id', UUID(True), ForeignKey(User.id), nullable=False, index=True
    )

    route = Column(
        'route', String, nullable=False
    )

    hit_datetime = Column(
        'datetime', DateTime, default=datetime.now(), nullable=False, index=True
    )

    ip_address = Column(
        'ip_address', String(16), nullable=False
    )

    user_input = Column(
        'user_input', String, default='', nullable=False
    )

    route_output = Column(
        'route_output', String, default=''
    )

    def __repr__(self) -> str:
        # TODO(Mike): Scrub user_input for certain variables and clear them out
        # EG[
        #   Password
        # ]
        return f'''
        <APILog(
            id={self.id},
            user_id={self.user_id},
            route={self.route},
            hit_datetime={self.hit_datetime},
            ip_address={self.ip_address},
            user_input={self.user_input},
            route_output={self.route_output}
        )
        '''

class Log(app.db.Model):
    __tablename__ = 'log'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False
    )

    time = Column(
        'time', DateTime, default=datetime.now(), nullable=False, index=True
    )

    level = Column(
        'level', String, nullable=False, default='DEBUG'
    )

    filename = Column(
        'filename', String, nullable=True
    )

    filepath = Column(
        'filepath', String, nullable=True
    )

    line_number = Column(
        'line_number', Integer, nullable=True
    )

    logger_name = Column(
        'logger_name', String, nullable=True
    )

    message = Column(
        'message', String, nullable=False
    )