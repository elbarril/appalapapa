"""
Main routes for the application.

Handles home page and general routes.
"""

from flask import Blueprint, redirect, url_for
from flask_login import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    """Redirect to patients dashboard."""
    return redirect(url_for("patients.index"))


@main_bp.route("/health")
def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        JSON with health status
    """
    from app.extensions import db

    try:
        # Check database connection
        db.session.execute(db.text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    status = "healthy" if db_status == "ok" else "unhealthy"
    http_code = 200 if status == "healthy" else 503

    return {"status": status, "database": db_status, "version": "2.0.0"}, http_code
