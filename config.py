"""
Configuration settings for Flask ML Application
Supports both development and production environments
"""
import os
from pathlib import Path

class Config:
    """Base configuration class"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Application settings
    BASE_DIR = Path(__file__).parent.absolute()
    DATA_DIR = BASE_DIR
    
    # Default hub coordinates (Paris)
    DEFAULT_HUB_LAT = float(os.environ.get('HUB_LAT', '48.866'))
    DEFAULT_HUB_LON = float(os.environ.get('HUB_LON', '2.400'))
    
    # Default priority weights
    DEFAULT_W_URGENCY = float(os.environ.get('W_URGENCY', '0.60'))
    DEFAULT_W_DEMAND = float(os.environ.get('W_DEMAND', '0.25'))
    DEFAULT_W_PROXIMITY = float(os.environ.get('W_PROXIMITY', '0.15'))
    
    # ML Model settings
    DEFAULT_N_VEHICLES = int(os.environ.get('N_VEHICLES', '200'))
    DEFAULT_RANDOM_SEED = int(os.environ.get('RANDOM_SEED', '42'))
    
    # File paths
    DISPATCH_FILE = DATA_DIR / 'dispatch_list.csv'
    TOP50_FILE = DATA_DIR / 'top_50_dispatch.csv'
    SYNTHETIC_FILE = DATA_DIR / 'synthetic_gbfs.csv'
    
    # Security settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    FLASK_ENV = 'development'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        app.logger.info('Running in DEVELOPMENT mode')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    FLASK_ENV = 'production'
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        app.logger.info('Running in PRODUCTION mode')

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Testing-specific settings
    FLASK_ENV = 'testing'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        app.logger.info('Running in TESTING mode')

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
