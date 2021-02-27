from pathlib import Path
import logging
class Config:
    DEBUG = False
    TESTING = False
    HOST = '127.0.0.1'
    PORT = 5000
    POOL_SIZE = 20
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/signals/
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Location of Database init/population scripts. This can be overriden but it does need to be a Path object
    DB_POPULATION_SCRIPTS_LOCATIONS = Path('backend') / 'database'/ 'setup' / 'init_scripts' /'db_scripts'
    # Sets the log level filter
    LOG_LEVEL = logging.INFO
    LOG_LOCATION = Path('var') / 'log' / 'football-sim'

class Development(Config):
    # If enabled, this will auto create any triggers found in backend/database/setup/triggers. See backend/database/setup/triggers/create_triggers.py for more details
    WATCH_TRIGGERS = True
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    LOG_LOCATION = Path('backend') / 'logs'


class Testing(Config):
    TESTING = True


class Production(Config):
    pass
