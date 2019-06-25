# flaskr/config.py
import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    # MONGODB_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGODB_SETTINGS = {
        'db': 'devDB',
        'host': 'mongo',
        'port': 27017,
    }
    DEBUG_TB_ENABLED = True
    BCRYPT_LOG_ROUNDS = 4
    SECRET_KEY = 'dev'


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'testDB',
        'host': 'mongo',
        'port': 27017
    }
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3
    SECRET_KEY = 'test'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    MONGODB_SETTINGS = {
        'db': 'prodDB',
        'host': 'mongo',
        'port': 27017,
    }
    DEBUG = False
    SECRET_KEY = None
