"""
Audit Log model for tracking all changes to data.

Used for regulatory compliance and debugging.
"""

from datetime import datetime
from typing import Optional, Any, Dict

from app.extensions import db
from app.utils.constants import AuditAction


class AuditLog(db.Model):
    """
    Audit Log model.

    Tracks all create, update, and delete operations on data.
    This is essential for regulatory compliance (GDPR, HIPAA)
    and debugging data issues.

    Attributes:
        id: Primary key
        user_id: User who performed the action
        action: Type of action (CREATE, UPDATE, DELETE, etc.)
        table_name: Name of the affected table
        record_id: ID of the affected record
        old_values: JSON of values before change
        new_values: JSON of values after change
        ip_address: Client IP address
        user_agent: Client user agent string
        timestamp: When the action occurred
    """

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True, index=True
    )
    action = db.Column(db.String(50), nullable=False, index=True)
    table_name = db.Column(db.String(100), nullable=False, index=True)
    record_id = db.Column(db.Integer, nullable=True)
    old_values = db.Column(db.JSON, nullable=True)
    new_values = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 max length
    user_agent = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    # Relationships
    user = db.relationship("User", backref="audit_logs")

    def __repr__(self) -> str:
        return f"<AuditLog {self.action} on {self.table_name}:{self.record_id}>"

    @classmethod
    def log(
        cls,
        action: str,
        table_name: str,
        record_id: Optional[int] = None,
        user_id: Optional[int] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> "AuditLog":
        """
        Create a new audit log entry.

        Args:
            action: Type of action (use AuditAction constants)
            table_name: Name of the affected table
            record_id: ID of the affected record
            user_id: ID of user performing the action
            old_values: Dictionary of old values
            new_values: Dictionary of new values
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            New AuditLog entry (automatically committed)
        """
        log = cls(
            action=action,
            table_name=table_name,
            record_id=record_id,
            user_id=user_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.session.add(log)
        db.session.commit()
        return log

    @classmethod
    def log_create(
        cls,
        table_name: str,
        record_id: int,
        new_values: Dict[str, Any],
        user_id: Optional[int] = None,
        **kwargs,
    ) -> "AuditLog":
        """Log a CREATE action."""
        return cls.log(
            action=AuditAction.CREATE,
            table_name=table_name,
            record_id=record_id,
            user_id=user_id,
            new_values=new_values,
            **kwargs,
        )

    @classmethod
    def log_update(
        cls,
        table_name: str,
        record_id: int,
        old_values: Dict[str, Any],
        new_values: Dict[str, Any],
        user_id: Optional[int] = None,
        **kwargs,
    ) -> "AuditLog":
        """Log an UPDATE action."""
        return cls.log(
            action=AuditAction.UPDATE,
            table_name=table_name,
            record_id=record_id,
            user_id=user_id,
            old_values=old_values,
            new_values=new_values,
            **kwargs,
        )

    @classmethod
    def log_delete(
        cls,
        table_name: str,
        record_id: int,
        old_values: Dict[str, Any],
        user_id: Optional[int] = None,
        **kwargs,
    ) -> "AuditLog":
        """Log a DELETE action."""
        return cls.log(
            action=AuditAction.DELETE,
            table_name=table_name,
            record_id=record_id,
            user_id=user_id,
            old_values=old_values,
            **kwargs,
        )

    @classmethod
    def log_login(cls, user_id: int, success: bool = True, **kwargs) -> "AuditLog":
        """Log a login attempt."""
        action = AuditAction.LOGIN if success else AuditAction.LOGIN_FAILED
        return cls.log(
            action=action,
            table_name="users",
            record_id=user_id,
            user_id=user_id if success else None,
            **kwargs,
        )

    @classmethod
    def get_for_record(cls, table_name: str, record_id: int, limit: int = 50):
        """
        Get audit log entries for a specific record.

        Args:
            table_name: Name of the table
            record_id: ID of the record
            limit: Maximum entries to return

        Returns:
            Query for audit log entries
        """
        return (
            cls.query.filter_by(table_name=table_name, record_id=record_id)
            .order_by(cls.timestamp.desc())
            .limit(limit)
        )

    @classmethod
    def get_for_user(cls, user_id: int, limit: int = 100):
        """
        Get audit log entries for a specific user.

        Args:
            user_id: User's ID
            limit: Maximum entries to return

        Returns:
            Query for audit log entries
        """
        return (
            cls.query.filter_by(user_id=user_id)
            .order_by(cls.timestamp.desc())
            .limit(limit)
        )

    def to_dict(self) -> dict:
        """Convert audit log to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "table_name": self.table_name,
            "record_id": self.record_id,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
