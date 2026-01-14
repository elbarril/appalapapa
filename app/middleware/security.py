"""
Security middleware.

Provides security headers and CORS configuration.
"""
from flask import request, g
from functools import wraps


def add_security_headers(response):
    """
    Add security headers to all responses.
    
    Call this in app factory: app.after_request(add_security_headers)
    """
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS filter
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Referrer policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Content Security Policy (customize as needed)
    # response.headers['Content-Security-Policy'] = "default-src 'self'"
    
    return response


def log_request():
    """
    Log incoming requests for debugging/monitoring.
    
    Call this in app factory: app.before_request(log_request)
    """
    from flask import current_app
    from flask_login import current_user
    
    user_id = current_user.id if current_user.is_authenticated else 'anonymous'
    current_app.logger.debug(
        f"Request: {request.method} {request.path} - User: {user_id}"
    )


def track_request_time():
    """
    Track request processing time.
    
    Call in before_request to start timer.
    """
    import time
    g.start_time = time.time()


def log_request_time(response):
    """
    Log request processing time.
    
    Call in after_request to log elapsed time.
    """
    import time
    from flask import current_app
    
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        if elapsed > 1.0:  # Log slow requests (>1 second)
            current_app.logger.warning(
                f"Slow request: {request.method} {request.path} - {elapsed:.2f}s"
            )
    
    return response
