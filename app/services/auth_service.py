"""
Authentication service for user management.

Handles login, registration, password reset, and session management.
"""

from typing import Optional, Tuple
from datetime import datetime
import logging
from flask import current_app, request

from app.extensions import db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.utils.constants import AuditAction, UserRole

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class RegistrationError(Exception):
    """Raised when registration fails."""

    pass


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def authenticate(email: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        Authenticate a user with email and password.

        Args:
            email: User's email address
            password: Plain text password

        Returns:
            Tuple of (success, user, message)
        """
        if not email or not password:
            return False, None, "Email y contraseña son requeridos."

        user = User.get_by_email(email)

        if user is None:
            logger.warning(f"Login attempt for non-existent email: {email}")
            return False, None, "Email o contraseña incorrecto."

        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {email}")
            return False, None, "Esta cuenta está desactivada."

        if user.is_deleted:
            logger.warning(f"Login attempt for deleted user: {email}")
            return False, None, "Email o contraseña incorrecto."

        if not user.check_password(password):
            # Log failed attempt
            AuditLog.log(
                action=AuditAction.LOGIN_FAILED,
                table_name="users",
                record_id=user.id,
                ip_address=request.remote_addr if request else None,
                user_agent=request.user_agent.string if request else None,
            )
            logger.warning(f"Failed login attempt for user: {email}")
            return False, None, "Email o contraseña incorrecto."

        # Update last login
        user.update_last_login()
        db.session.commit()

        # Log successful login
        AuditLog.log(
            action=AuditAction.LOGIN,
            table_name="users",
            record_id=user.id,
            user_id=user.id,
            ip_address=request.remote_addr if request else None,
            user_agent=request.user_agent.string if request else None,
        )

        logger.info(f"Successful login for user: {email}")
        return True, user, "Ingresó correctamente."

    @staticmethod
    def register(
        email: str, password: str, role: str = UserRole.THERAPIST
    ) -> Tuple[bool, Optional[User], str]:
        """
        Register a new user.

        Args:
            email: User's email address
            password: Plain text password
            role: User role (default: therapist)

        Returns:
            Tuple of (success, user, message)
        """
        if not email or not password:
            return False, None, "Email y contraseña son requeridos."

        email = email.lower().strip()

        # Check allowed emails
        allowed_emails = current_app.config.get("ALLOWED_EMAILS", set())
        if allowed_emails and email not in allowed_emails:
            logger.warning(f"Registration attempt with unauthorized email: {email}")
            return False, None, "Este email no está autorizado para registrarse."

        # Check if email already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {email}")
            return False, None, "Este email ya está registrado."

        # Create user
        try:
            user = User.create_user(email, password, role)
            db.session.add(user)
            db.session.commit()

            # Audit log
            AuditLog.log_create(
                table_name="users",
                record_id=user.id,
                new_values={"email": email, "role": role},
                ip_address=request.remote_addr if request else None,
            )

            logger.info(f"New user registered: {email}")
            return True, user, "Cuenta creada con éxito. Ahora podés iniciar sesión."

        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error for {email}: {str(e)}")
            return False, None, "Error al crear la cuenta. Intente nuevamente."

    @staticmethod
    def reset_password(
        email: str, new_password: str, security_answer: str
    ) -> Tuple[bool, str]:
        """
        Reset user password with security question (legacy method).

        Args:
            email: User's email address
            new_password: New password
            security_answer: Answer to security question

        Returns:
            Tuple of (success, message)
        """
        # Legacy security check (to be replaced with email-based reset)
        if "-08-17" not in security_answer:
            logger.warning(f"Password reset failed (security): {email}")
            return False, "La respuesta a la pregunta de seguridad es incorrecta."

        user = User.get_by_email(email)
        if not user:
            logger.warning(f"Password reset for non-existent email: {email}")
            return False, "No existe una cuenta registrada con ese email."

        try:
            old_hash = user.password_hash
            user.set_password(new_password)
            db.session.commit()

            # Audit log
            AuditLog.log(
                action=AuditAction.PASSWORD_RESET,
                table_name="users",
                record_id=user.id,
                user_id=user.id,
                old_values={"password_hash": "REDACTED"},
                new_values={"password_hash": "REDACTED"},
                ip_address=request.remote_addr if request else None,
            )

            logger.info(f"Password reset successful for: {email}")
            return True, "Contraseña actualizada correctamente."

        except Exception as e:
            db.session.rollback()
            logger.error(f"Password reset error for {email}: {str(e)}")
            return False, "Error al actualizar la contraseña. Intente nuevamente."

    @staticmethod
    def change_password(
        user: User, current_password: str, new_password: str
    ) -> Tuple[bool, str]:
        """
        Change password for logged-in user.

        Args:
            user: Current user
            current_password: Current password for verification
            new_password: New password

        Returns:
            Tuple of (success, message)
        """
        if not user.check_password(current_password):
            return False, "La contraseña actual es incorrecta."

        try:
            user.set_password(new_password)
            db.session.commit()

            AuditLog.log(
                action=AuditAction.UPDATE,
                table_name="users",
                record_id=user.id,
                user_id=user.id,
                old_values={"password_hash": "REDACTED"},
                new_values={"password_hash": "REDACTED"},
                ip_address=request.remote_addr if request else None,
            )

            logger.info(f"Password changed for user: {user.email}")
            return True, "Contraseña actualizada correctamente."

        except Exception as e:
            db.session.rollback()
            logger.error(f"Password change error for {user.email}: {str(e)}")
            return False, "Error al cambiar la contraseña. Intente nuevamente."

    @staticmethod
    def logout(user: User) -> None:
        """
        Log user logout action.

        Args:
            user: User logging out
        """
        if user and user.is_authenticated:
            AuditLog.log(
                action=AuditAction.LOGOUT,
                table_name="users",
                record_id=user.id,
                user_id=user.id,
                ip_address=request.remote_addr if request else None,
            )
            logger.info(f"User logged out: {user.email}")
