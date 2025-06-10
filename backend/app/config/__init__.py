"""
Initialize the configuration package.

This module centralizes the application's configuration settings and provides
utilities for managing different environments.
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file, if present
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DATABASE_URL = 'sqlite:///test.db'

# Export the appropriate configuration based on the environment
environment = os.getenv('FLASK_ENV', 'development').lower()
if environment == 'production':
    current_config = ProductionConfig()
elif environment == 'testing':
    current_config = TestingConfig()
else:
    current_config = DevelopmentConfig()
