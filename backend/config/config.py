class Config:
    DEBUG = False
    TESTING = False
    HOST = "127.0.0.1"
    PORT = 5000
    POOL_SIZE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WATCH_TRIGGERS = True


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True


class Production(Config):
    pass
