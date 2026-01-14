"""
Global error handlers.

Provides custom error pages and logging for all HTTP errors.
"""

from flask import render_template, request, current_app


def handle_400(error):
    """Handle 400 Bad Request errors."""
    current_app.logger.warning(f"400 error: {request.url} - {error}")
    return render_template("errors/400.html", error=error), 400


def handle_403(error):
    """Handle 403 Forbidden errors."""
    current_app.logger.warning(
        f"403 error: {request.url} - User attempted unauthorized access"
    )
    return render_template("errors/403.html", error=error), 403


def handle_404(error):
    """Handle 404 Not Found errors."""
    current_app.logger.info(f"404 error: {request.url}")
    return render_template("errors/404.html", error=error), 404


def handle_500(error):
    """Handle 500 Internal Server errors."""
    current_app.logger.error(f"500 error: {request.url} - {error}", exc_info=True)
    return render_template("errors/500.html", error=error), 500


def handle_csrf_error(error):
    """Handle CSRF token errors."""
    current_app.logger.warning(f"CSRF error: {request.url} - {error.description}")
    return (
        render_template(
            "errors/403.html",
            error="El formulario ha expirado. Por favor, actualiza la página e intenta nuevamente.",
        ),
        403,
    )


def register_error_handlers(app):
    """Register all error handlers with the app."""
    app.register_error_handler(400, handle_400)
    app.register_error_handler(403, handle_403)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
