"""
REST API v1 Blueprint.

Provides JSON API endpoints for mobile and external integrations.
"""

from flask import Blueprint

api_v1_bp = Blueprint("api_v1", __name__)

# Import and register resources
from app.api.v1 import resources  # noqa
