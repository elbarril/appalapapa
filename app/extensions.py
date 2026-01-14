"""
Flask extensions initialization.

All Flask extensions are initialized here and imported by the app factory.
This prevents circular imports and allows for easier testing.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Database ORM
db = SQLAlchemy()

# Database migrations
migrate = Migrate()

# User session management
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Ingresa con tu usuario para ver esta página."
login_manager.login_message_category = "warning"
# Session protection set during app initialization based on config

# CSRF protection
csrf = CSRFProtect()

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    from app.models.user import User

    return User.query.get(int(user_id))
