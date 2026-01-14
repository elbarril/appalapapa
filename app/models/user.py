"""
User model for authentication and authorization.
"""

from datetime import datetime
from typing import List, Optional

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.mixins import SoftDeleteMixin, TimestampMixin
from app.utils.constants import UserRole


class User(UserMixin, TimestampMixin, SoftDeleteMixin, db.Model):
    """
    User model for authentication.

    Attributes:
        id: Primary key
        email: Unique email address (used for login)
        password_hash: Hashed password (never store plaintext)
        role: User role for authorization (admin, therapist, viewer)
        is_active: Whether user can log in
        last_login_at: Timestamp of last successful login
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default=UserRole.THERAPIST, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    persons = db.relationship("Person", backref="owner", lazy="dynamic", foreign_keys="Person.created_by_id")

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def set_password(self, password: str) -> None:
        """
        Hash and store password.

        Args:
            password: Plain text password to hash
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify password against stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def update_last_login(self) -> None:
        """Update the last login timestamp to now."""
        self.last_login_at = datetime.utcnow()

    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN

    @property
    def is_therapist(self) -> bool:
        """Check if user has therapist role."""
        return self.role == UserRole.THERAPIST

    @property
    def is_viewer(self) -> bool:
        """Check if user has viewer role."""
        return self.role == UserRole.VIEWER

    def has_role(self, role: str) -> bool:
        """
        Check if user has a specific role.

        Args:
            role: Role to check

        Returns:
            True if user has the role
        """
        return self.role == role

    def has_any_role(self, *roles: str) -> bool:
        """
        Check if user has any of the specified roles.

        Args:
            *roles: Roles to check

        Returns:
            True if user has any of the roles
        """
        return self.role in roles

    def can_delete_patients(self) -> bool:
        """Check if user can delete patients."""
        return self.role in (UserRole.ADMIN, UserRole.THERAPIST)

    def can_manage_users(self) -> bool:
        """Check if user can manage other users."""
        return self.is_admin

    @classmethod
    def get_by_email(cls, email: str) -> Optional["User"]:
        """
        Get user by email address.

        Args:
            email: Email address to search for

        Returns:
            User instance or None if not found
        """
        return cls.query.filter_by(email=email.lower().strip()).first()

    @classmethod
    def create_user(cls, email: str, password: str, role: str = UserRole.THERAPIST) -> "User":
        """
        Create a new user with hashed password.

        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            role: User role

        Returns:
            New User instance (not yet committed to database)
        """
        user = cls(email=email.lower().strip(), role=role)
        user.set_password(password)
        return user
