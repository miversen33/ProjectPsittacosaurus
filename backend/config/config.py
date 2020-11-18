class Config:
    DATABASE_URI = 'sqlite:///memory'
    DEBUG = False
    TESTING = False
    HOST = '127.0.0.1'
    PORT = 5000
    POOL_SIZE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WATCH_TRIGGERS = True


class Development(Config):
    DATABASE_URI = 'postgres://football_dev:5rI5B!GOWhT$bom@bladebeat-server:5430'
    DEBUG = True


class Testing(Config):
    TESTING = True


class Production(Config):
    pass
