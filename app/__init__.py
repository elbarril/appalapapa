"""
Therapy Session Management Application.

A Flask-based web application for managing patient therapy sessions
with payment tracking, audit logging, and role-based access control.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask

from app.config import config
from app.extensions import csrf, db, limiter, login_manager, migrate


def create_app(config_name=None):
    """
    Application factory pattern.

    Creates and configures the Flask application instance.

    Args:
        config_name: Configuration to use ('development', 'testing', 'production')
                    If None, reads from FLASK_CONFIG environment variable.

    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    # Get the root directory (parent of app package)
    root_path = Path(__file__).parent.parent

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(root_path / "templates"),
        static_folder=str(root_path / "static"),
    )

    # Load configuration
    app.config.from_object(config[config_name])

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize Flask extensions
    register_extensions(app)

    # Register blueprints (routes)
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Register request middleware (security headers, caching)
    register_middleware(app)

    # Register CLI commands
    register_cli_commands(app)

    # Register template context processors
    register_context_processors(app)

    # Configure logging
    configure_logging(app)

    # Production-specific initialization
    if hasattr(config[config_name], "init_app"):
        config[config_name].init_app(app)

    return app


def register_extensions(app):
    """Initialize Flask extensions with the app."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Configure session protection based on environment
    login_manager.session_protection = app.config.get("SESSION_PROTECTION", "strong")

    # Configure rate limiter with app settings
    if app.config.get("RATELIMIT_ENABLED", True):
        limiter.init_app(app)


def register_blueprints(app):
    """Register all application blueprints."""
    from app.api.v1 import api_v1_bp
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.patients import patients_bp
    from app.routes.sessions import sessions_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(patients_bp, url_prefix="/patients")
    app.register_blueprint(sessions_bp, url_prefix="/sessions")
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")


def register_error_handlers(app):
    """Register global error handlers."""
    from app.middleware.error_handlers import (
        handle_400,
        handle_403,
        handle_404,
        handle_500,
        handle_csrf_error,
    )

    app.register_error_handler(400, handle_400)
    app.register_error_handler(403, handle_403)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)

    # CSRF error handler
    from flask_wtf.csrf import CSRFError

    app.register_error_handler(CSRFError, handle_csrf_error)


def register_middleware(app):
    """Register request/response middleware."""
    from app.middleware.security import add_cache_headers, add_security_headers

    # Add security headers to all responses
    app.after_request(add_security_headers)

    # Add cache headers for static assets (performance optimization)
    app.after_request(add_cache_headers)


def register_cli_commands(app):
    """Register custom CLI commands."""
    from app.cli import db_commands, user_commands

    app.cli.add_command(db_commands.db_cli)
    app.cli.add_command(user_commands.user_cli)


def register_context_processors(app):
    """Register template context processors."""
    from app.utils.constants import ALLOW_DELETE, FILTERS
    from app.utils.formatters import format_date, format_price

    @app.context_processor
    def utility_processor():
        """Add utility functions to template context."""
        return {
            "format_date": format_date,
            "format_price": format_price,
            "filters": FILTERS,
            "allow_delete": ALLOW_DELETE,
        }


def configure_logging(app):
    """Configure application logging."""
    if app.debug or app.testing:
        return

    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create file handler with rotation
    log_file = app.config.get("LOG_FILE", "logs/app.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=10)  # 10MB

    # Set log level
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))
    file_handler.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    file_handler.setFormatter(formatter)

    # Add handler to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)

    app.logger.info("Application startup")
