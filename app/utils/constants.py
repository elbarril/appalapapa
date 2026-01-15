"""
Application constants.

All magic numbers and strings should be defined here as named constants.
"""

import os

# =============================================================================
# Feature Flags
# =============================================================================
ALLOW_DELETE = os.environ.get("ALLOW_DELETE", "true").lower() == "true"

# =============================================================================
# Session Filters
# =============================================================================
ALL_FILTER = "all"
PENDING_FILTER = "pending"
PAID_FILTER = "paid"

FILTERS = [
    ("TODOS", ALL_FILTER),
    ("PENDIENTES", PENDING_FILTER),
    ("PAGADOS", PAID_FILTER),
]

# =============================================================================
# Pagination
# =============================================================================
DEFAULT_PAGE_SIZE = int(os.environ.get("ITEMS_PER_PAGE", 50))
MAX_PAGE_SIZE = 100

# =============================================================================
# Rate Limiting
# =============================================================================
AUTH_RATE_LIMIT = os.environ.get("RATE_LIMIT_AUTH", "5 per minute")
API_RATE_LIMIT = "60 per minute"

# =============================================================================
# Session Configuration
# =============================================================================
SESSION_LIFETIME_DAYS = int(os.environ.get("SESSION_LIFETIME_DAYS", 7))


# =============================================================================
# Audit Log Actions
# =============================================================================
class AuditAction:
    """Audit log action types."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SOFT_DELETE = "SOFT_DELETE"
    RESTORE = "RESTORE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    LOGIN_FAILED = "LOGIN_FAILED"
    PASSWORD_RESET = "PASSWORD_RESET"


# =============================================================================
# User Roles
# =============================================================================
class UserRole:
    """User role constants."""

    ADMIN = "admin"
    THERAPIST = "therapist"
    VIEWER = "viewer"


# =============================================================================
# Payment Status
# =============================================================================
class PaymentStatus:
    """Payment status constants."""

    PENDING = True
    PAID = False


# =============================================================================
# Flash Message Categories
# =============================================================================
class FlashCategory:
    """Flash message category constants for consistent styling."""

    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


# =============================================================================
# Validation Constants
# =============================================================================
MIN_PASSWORD_LENGTH = 8
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 255
MAX_PRICE = 1_000_000  # Maximum session price
MIN_PRICE = 0.01  # Minimum session price

# =============================================================================
# Date Formats
# =============================================================================
DATE_FORMAT_INPUT = "%Y-%m-%d"
DATE_FORMAT_DISPLAY = "%A %d/%m/%Y"
DATETIME_FORMAT_DISPLAY = "%d/%m/%Y %H:%M"

# Spanish day and month names (used explicitly for cross-platform consistency)
# Monday = 0, Sunday = 6 (matches Python's weekday())
SPANISH_DAYS = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]

# January = 0, December = 11 (for array indexing with month - 1)
SPANISH_MONTHS = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]
