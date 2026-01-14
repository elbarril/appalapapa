"""
Custom decorators for routes and functions.

Provides authentication, authorization, and utility decorators.
"""
from functools import wraps
from flask import flash, redirect, url_for, request, current_app, abort
from flask_login import current_user

from app.utils.constants import FlashCategory, UserRole


def login_required_custom(f):
    """
    Custom login required decorator with Spanish message.
    
    Note: Prefer using flask_login.login_required instead.
    This is kept for backward compatibility.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Ingresa con tu usuario para ver esta página.', FlashCategory.WARNING)
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Require admin role for the decorated route.
    
    Returns 403 Forbidden if user is not an admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Ingresa con tu usuario para ver esta página.', FlashCategory.WARNING)
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_admin:
            current_app.logger.warning(
                f'Unauthorized admin access attempt by user {current_user.id}'
            )
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """
    Require specific role(s) for the decorated route.
    
    Args:
        *roles: One or more role strings (e.g., UserRole.ADMIN, UserRole.THERAPIST)
    
    Usage:
        @role_required(UserRole.ADMIN, UserRole.THERAPIST)
        def some_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Ingresa con tu usuario para ver esta página.', FlashCategory.WARNING)
                return redirect(url_for('auth.login', next=request.url))
            
            if not current_user.has_any_role(*roles):
                current_app.logger.warning(
                    f'Unauthorized access attempt by user {current_user.id} '
                    f'(required roles: {roles}, user role: {current_user.role})'
                )
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def confirmed_required(f):
    """
    Require email confirmation for the decorated route.
    
    Redirects to confirmation page if email is not confirmed.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Ingresa con tu usuario para ver esta página.', FlashCategory.WARNING)
            return redirect(url_for('auth.login', next=request.url))
        
        if hasattr(current_user, 'is_confirmed') and not current_user.is_confirmed:
            flash('Por favor confirma tu email antes de continuar.', FlashCategory.WARNING)
            return redirect(url_for('auth.unconfirmed'))
        
        return f(*args, **kwargs)
    return decorated_function


def log_activity(action: str):
    """
    Log user activity for audit purposes.
    
    Args:
        action: Description of the action being performed
    
    Usage:
        @log_activity('Viewed patient list')
        def list_patients():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = current_user.id if current_user.is_authenticated else 'anonymous'
            current_app.logger.info(
                f"Activity: {action} | User: {user_id} | "
                f"Path: {request.path} | Method: {request.method}"
            )
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def handle_exceptions(f):
    """
    Handle exceptions gracefully with logging and user-friendly messages.
    
    Catches exceptions, logs them, and shows a flash message.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(
                f"Exception in {f.__name__}: {str(e)}",
                exc_info=True
            )
            flash('Ocurrió un error. Por favor intente nuevamente.', FlashCategory.ERROR)
            return redirect(request.referrer or url_for('main.index'))
    return decorated_function
