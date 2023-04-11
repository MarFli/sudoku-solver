class Config(object):
    TESTING = False
    DEBUG = False

class ProductionConfig(Config):
    ENV = 'production'

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    ENV = 'development'
    TESTING = True
    DEBUG = True
