# DEBUG=True
# TESTING=True | False
# SECRET_KEY
# LOGGER_NAME
# SERVER_NAME
# APPLICATION_ROOT


class Config(object):
    APPLICATION_ROOT = "/var/local/Comp4350/ESA"
    SECRET_KEY = 'This is a very secure secret key'

class ProdConfig(Config):
    ENV = "Prod"
    DEBUG = True
    
class DevConfig(Config):
    ENV = "Dev"
    DEBUG = True
