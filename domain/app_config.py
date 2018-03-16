import configparser

DEFAULT_CONFIG = 'config/app.ini'

def get_config():    
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG)

    return config