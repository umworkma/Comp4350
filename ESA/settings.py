# DEBUG=True
# TESTING=True | False
# SECRET_KEY
# LOGGER_NAME
# SERVER_NAME
# APPLICATION_ROOT


class Config(object):
    APPLICATION_ROOT = "/var/local/Comp4350/ESA"

class ProdConfig(Config):
    ENV = "Prod"
    
class DevConfig(Config):
    ENV = "Dev"
    DEBUG = True
