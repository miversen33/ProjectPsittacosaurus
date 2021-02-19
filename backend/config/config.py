class Config:
    DEBUG = False
    TESTING = False
    HOST = '127.0.0.1'
    PORT = 5000
    POOL_SIZE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WATCH_TRIGGERS = True


class Development(Config):
    # If enabled, this will auto create any triggers found in backend/database/setup/triggers. See backend/database/setup/triggers/create_triggers.py for more details
    WATCH_TRIGGERS = True
    DEBUG = True


class Testing(Config):
    TESTING = True


class Production(Config):
    pass
