"""
Flask application configuration classes.

Supports multiple environments: development, testing, production.
All sensitive values should be loaded from environment variables.
"""
import os
from datetime import timedelta
from pathlib import Path

# Load environment variables from .env file before any config is read
from dotenv import load_dotenv

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from the project root
load_dotenv(BASE_DIR / '.env')


class Config:
    """Base configuration with default values."""
    
    # Flask core
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before use
    }
    
    # Session security
    PERMANENT_SESSION_LIFETIME = timedelta(
        days=int(os.environ.get('SESSION_LIFETIME_DAYS', 7))
    )
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # No JS access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    SESSION_PROTECTION = 'strong'  # Flask-Login session protection
    
    # CSRF protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No expiration
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # Application settings
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 50))
    ALLOW_DELETE = os.environ.get('ALLOW_DELETE', 'true').lower() == 'true'
    
    # Allowed emails for registration (comma-separated)
    ALLOWED_EMAILS = set(
        email.strip() 
        for email in os.environ.get('ALLOWED_EMAILS', '').split(',') 
        if email.strip()
    )
    
    # File uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = str(BASE_DIR / 'uploads')
    
    # Sentry error monitoring
    SENTRY_DSN = os.environ.get('SENTRY_DSN')


class DevelopmentConfig(Config):
    """Development configuration with debug features."""
    
    DEBUG = True
    TESTING = False
    
    # SQLite for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{BASE_DIR / 'instance' / 'database.db'}"
    
    # Show SQL queries in console
    SQLALCHEMY_ECHO = True
    
    # Allow HTTP in development (no HTTPS requirement)
    SESSION_COOKIE_SECURE = False
    
    # Relaxed session protection for development (prevents logout on IP/user-agent changes)
    SESSION_PROTECTION = 'basic'
    
    # More verbose logging
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """Testing configuration with in-memory database."""
    
    TESTING = True
    DEBUG = True
    
    # In-memory SQLite for fast tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF in tests for easier form submission
    WTF_CSRF_ENABLED = False
    
    # Disable rate limiting in tests
    RATELIMIT_ENABLED = False
    
    # Allow HTTP
    SESSION_COOKIE_SECURE = False
    
    # Relaxed session protection for testing
    SESSION_PROTECTION = 'basic'
    
    # Fast password hashing for tests
    BCRYPT_LOG_ROUNDS = 4
    
    # Test-specific settings
    SERVER_NAME = 'localhost'
    
    # Allow all emails in tests
    ALLOWED_EMAILS = set()


class ProductionConfig(Config):
    """Production configuration with strict security."""
    
    DEBUG = False
    TESTING = False
    
    # PostgreSQL required in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Connection pooling for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # Strict session security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Production logging level
    LOG_LEVEL = 'WARNING'
    
    @classmethod
    def init_app(cls, app):
        """Production-specific initialization."""
        # Initialize Sentry if DSN is configured
        if cls.SENTRY_DSN:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration
            
            sentry_sdk.init(
                dsn=cls.SENTRY_DSN,
                integrations=[FlaskIntegration()],
                traces_sample_rate=0.1,
                environment='production'
            )


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration class based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
