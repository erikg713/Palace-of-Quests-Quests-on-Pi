"""
Configuration management for Palace of Quests application.

Provides environment-specific configuration classes with validation
and type safety.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class DatabaseConfig:
    """Database configuration with connection pooling options."""
    uri: str
    track_modifications: bool = False
    engine_options: Dict[str, Any] = field(default_factory=lambda: {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0,
        'echo': False
    })


@dataclass 
class SecurityConfig:
    """Security-related configuration options."""
    secret_key: Optional[str] = None
    session_cookie_secure: bool = True
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = 'Lax'
    csrf_enabled: bool = True


class BaseConfig:
    """Base configuration with common settings."""
    
    # Flask settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @classmethod
    def get_database_uri(cls) -> str:
        """Get database URI with proper format handling."""
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        # Handle Heroku postgres URL format
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
        return db_url


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    SESSION_COOKIE_SECURE = False
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        **BaseConfig.SQLALCHEMY_ENGINE_OPTIONS,
        'echo': True  # Enable SQL query logging in development
    }


class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}


def get_config(config_name: Optional[str] = None) -> type:
    """
    Get configuration class for specified environment.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Configuration class for the specified environment
    """
    env = config_name or os.getenv('FLASK_ENV', 'production')
    return config_map.get(env, config_map['default'])
import os
from datetime import timedelta


class BaseConfig:
    """Base configuration with common settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Pi Network Configuration
    PI_NETWORK_API_KEY = os.environ.get('PI_NETWORK_API_KEY')
    PI_NETWORK_SANDBOX = os.environ.get('PI_NETWORK_SANDBOX', 'true').lower() == 'true'
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    RATELIMIT_DEFAULT = "100 per hour"
    
    # Game Configuration
    MAX_PLAYER_LEVEL = 250
    BASE_XP_REQUIREMENT = 100
    XP_MULTIPLIER = 1.5
    
    # Marketplace Settings
    TRANSACTION_FEE_PERCENT = 0.05
    MIN_LISTING_PRICE = 0.01


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:password@localhost/palace_of_quests_dev'
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql://postgres:password@localhost/palace_of_quests_test'


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
