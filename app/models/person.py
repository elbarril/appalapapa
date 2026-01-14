"""
Person (Patient) model for therapy session management.
"""

from datetime import datetime
from typing import List, Optional

from app.extensions import db
from app.models.mixins import AuditMixin, SoftDeleteMixin, TimestampMixin


class Person(TimestampMixin, SoftDeleteMixin, AuditMixin, db.Model):
    """
    Person (Patient) model.

    Represents a patient who attends therapy sessions.

    Attributes:
        id: Primary key
        name: Patient's name (unique)
        notes: Optional notes about the patient
        is_active: Whether the patient is currently active
    """

    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    notes = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    therapy_sessions = db.relationship("TherapySession", backref="person", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Person {self.name}>"

    @property
    def session_count(self) -> int:
        """Get total number of sessions for this person."""
        return self.therapy_sessions.count()

    @property
    def pending_sessions(self):
        """Get query for pending (unpaid) sessions."""
        from app.models.session import TherapySession

        return self.therapy_sessions.filter_by(pending=True)

    @property
    def paid_sessions(self):
        """Get query for paid sessions."""
        from app.models.session import TherapySession

        return self.therapy_sessions.filter_by(pending=False)

    @property
    def pending_count(self) -> int:
        """Get count of pending sessions."""
        return self.pending_sessions.count()

    @property
    def pending_total(self) -> float:
        """Calculate total amount pending for this person."""
        return sum(s.session_price for s in self.pending_sessions.all())

    @property
    def total_paid(self) -> float:
        """Calculate total amount paid by this person."""
        return sum(s.session_price for s in self.paid_sessions.all())

    @property
    def total_sessions_value(self) -> float:
        """Calculate total value of all sessions."""
        return sum(s.session_price for s in self.therapy_sessions.all())

    @classmethod
    def get_by_name(cls, name: str) -> Optional["Person"]:
        """
        Get person by name.

        Args:
            name: Person's name to search for

        Returns:
            Person instance or None if not found
        """
        return cls.query_active().filter_by(name=name).first()

    @classmethod
    def create_person(cls, name: str, created_by_id: Optional[int] = None) -> "Person":
        """
        Create a new person.

        Args:
            name: Person's name
            created_by_id: ID of user creating the person

        Returns:
            New Person instance (not yet committed to database)
        """
        person = cls(name=name.strip(), created_by_id=created_by_id)
        return person

    @classmethod
    def get_all_active(cls, order_by_name: bool = True):
        """
        Get all active (non-deleted) persons.

        Args:
            order_by_name: Whether to order by name

        Returns:
            Query for active persons
        """
        query = cls.query_active()
        if order_by_name:
            query = query.order_by(cls.name)
        return query

    def to_dict(self) -> dict:
        """Convert person to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "notes": self.notes,
            "is_active": self.is_active,
            "session_count": self.session_count,
            "pending_count": self.pending_count,
            "pending_total": self.pending_total,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
