import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'firebox')
    DB_USER = os.environ.get('DB_USER', 'firebox')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.environ.get('LOG_FORMAT', 'json')
    LOG_DIR = os.environ.get('LOG_DIR', '/app/logs')
    
    # Application configuration
    HOST_IP = os.environ.get('HOST_IP', 'localhost')
    
    # Gateway configuration
    GATEWAY_CHECK_INTERVAL = int(os.environ.get('GATEWAY_CHECK_INTERVAL', 30))
    GATEWAY_TIMEOUT = int(os.environ.get('GATEWAY_TIMEOUT', 10))
    
    # Trial reset configuration
    SELENIUM_HEADLESS = os.environ.get('SELENIUM_HEADLESS', 'true').lower() == 'true'
    SELENIUM_TIMEOUT = int(os.environ.get('SELENIUM_TIMEOUT', 30))
    RESET_MAX_RETRIES = int(os.environ.get('RESET_MAX_RETRIES', 3))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}