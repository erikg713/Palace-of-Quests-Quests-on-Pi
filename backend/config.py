"""
Configuration management for Palace of Quests (Pi Quest) application.

This module provides environment-specific configuration classes
with validation and type safety. All critical environment variables
are validated at startup for reliability and security.
"""

import os
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Dict, Optional

# --- Utility ---

def require_env_var(var_name: str, default: Optional[Any] = None, secret: bool = False) -> Any:
    """Fetch an environment variable or raise if not set (unless default provided)."""
    value = os.environ.get(var_name, default)
    if value is None:
        raise RuntimeError(
            f"Required environment variable '{var_name}' is not set."
            + (" (Secret)" if secret else "")
        )
    return value

# --- Dataclasses for grouping config if needed elsewhere ---

@dataclass(frozen=True)
class DatabaseConfig:
    """Database configuration including pooling options."""
    uri: str
    track_modifications: bool = False
    engine_options: Dict[str, Any] = field(default_factory=lambda: {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0,
        'echo': False,
    })

@dataclass(frozen=True)
class SecurityConfig:
    """Security-related configuration options."""
    secret_key: str
    session_cookie_secure: bool = True
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = 'Lax'
    csrf_enabled: bool = True

# --- Main Config Classes ---

class BaseConfig:
    """Base configuration with common settings."""

    # Flask settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    # Security
    SECRET_KEY = require_env_var('SECRET_KEY', 'dev-secret-key', secret=True)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_ENABLED = True

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0,
    }

    # JWT (for authentication)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Pi Network
    PI_NETWORK_API_KEY = require_env_var('PI_NETWORK_API_KEY', secret=True)
    PI_NETWORK_SANDBOX = os.environ.get('PI_NETWORK_SANDBOX', 'true').lower() == 'true'

    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    RATELIMIT_DEFAULT = "100 per hour"

    # Game and Marketplace
    MAX_PLAYER_LEVEL = 250
    BASE_XP_REQUIREMENT = 100
    XP_MULTIPLIER = 1.5
    TRANSACTION_FEE_PERCENT = 0.05
    MIN_LISTING_PRICE = 0.01

    @classmethod
    def get_database_uri(cls) -> str:
        """
        Get the SQLAlchemy database URI, handling possible legacy URLs.
        """
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            raise RuntimeError("DATABASE_URL environment variable is required.")
        # Heroku compatibility
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return db_url

class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:password@localhost/palace_of_quests_dev'
    SQLALCHEMY_ENGINE_OPTIONS = {
        **BaseConfig.SQLALCHEMY_ENGINE_OPTIONS,
        'echo': True  # Log SQL queries in development
    }

class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = BaseConfig.get_database_uri()
    # Security: enforce secure cookies in production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False

# --- Config Map and Factory ---

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}

def get_config(config_name: Optional[str] = None) -> type:
    """
    Retrieve the configuration class for the specified environment.
    Args:
        config_name: Environment name (development, production, testing)
    Returns:
        Config class corresponding to the environment
    """
    env = config_name or os.environ.get('FLASK_ENV', 'production').lower()
    return config_map.get(env, config_map['default'])
