"""
Model mixins for common functionality.

These mixins can be added to any model to provide shared functionality
like timestamps, soft deletes, and audit tracking.
"""

from datetime import datetime
from typing import Optional

from app.extensions import db


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at columns to a model.

    Usage:
        class MyModel(db.Model, TimestampMixin):
            pass
    """

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    """
    Mixin that adds soft delete functionality to a model.

    Instead of permanently deleting records, they are marked as deleted
    with a timestamp. This allows for data recovery and audit trails.

    Usage:
        class MyModel(db.Model, SoftDeleteMixin):
            pass

        # Soft delete
        record.soft_delete()

        # Restore
        record.restore()

        # Query only active records
        MyModel.query_active().all()
    """

    deleted_at = db.Column(db.DateTime, nullable=True, index=True)
    deleted_by_id = db.Column(db.Integer, nullable=True)

    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted."""
        return self.deleted_at is not None

    def soft_delete(self, user_id: Optional[int] = None) -> None:
        """
        Mark record as deleted without removing from database.

        Args:
            user_id: ID of user performing the deletion
        """
        self.deleted_at = datetime.utcnow()
        if user_id:
            self.deleted_by_id = user_id

    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.deleted_by_id = None

    @classmethod
    def query_active(cls):
        """
        Return query for non-deleted records only.

        Returns:
            SQLAlchemy query filtered to exclude deleted records
        """
        return cls.query.filter(cls.deleted_at.is_(None))

    @classmethod
    def query_deleted(cls):
        """
        Return query for deleted records only.

        Returns:
            SQLAlchemy query filtered to only deleted records
        """
        return cls.query.filter(cls.deleted_at.isnot(None))


class AuditMixin:
    """
    Mixin that tracks who created and modified a record.

    Usage:
        class MyModel(db.Model, AuditMixin, TimestampMixin):
            pass
    """

    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    updated_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def set_created_by(self, user_id: int) -> None:
        """Set the user who created this record."""
        self.created_by_id = user_id

    def set_updated_by(self, user_id: int) -> None:
        """Set the user who last updated this record."""
        self.updated_by_id = user_id
