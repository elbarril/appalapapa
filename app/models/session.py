"""
Therapy Session model for tracking appointments and payments.
"""

from typing import Optional, List
from datetime import datetime, date

from app.extensions import db
from app.models.mixins import TimestampMixin, SoftDeleteMixin, AuditMixin


class TherapySession(TimestampMixin, SoftDeleteMixin, AuditMixin, db.Model):
    """
    Therapy Session model.

    Represents a single therapy session with a patient.

    Attributes:
        id: Primary key
        person_id: Foreign key to Person
        session_date: Date of the session
        session_price: Price/cost of the session
        pending: Whether payment is pending (True) or paid (False)
        notes: Optional notes about the session
    """

    __tablename__ = "therapy_sessions"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(
        db.Integer,
        db.ForeignKey("persons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_date = db.Column(db.Date, nullable=False, index=True)
    session_price = db.Column(db.Float, nullable=False)
    pending = db.Column(db.Boolean, default=True, nullable=False, index=True)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"<TherapySession {self.id} - {self.session_date}>"

    @property
    def is_pending(self) -> bool:
        """Check if session payment is pending."""
        return self.pending

    @property
    def is_paid(self) -> bool:
        """Check if session is paid."""
        return not self.pending

    @property
    def status_text(self) -> str:
        """Get human-readable status in Spanish."""
        return "Pendiente" if self.pending else "Pagado"

    def mark_as_paid(self, user_id: Optional[int] = None) -> None:
        """Mark session as paid."""
        self.pending = False
        if user_id:
            self.updated_by_id = user_id

    def mark_as_pending(self, user_id: Optional[int] = None) -> None:
        """Mark session as pending."""
        self.pending = True
        if user_id:
            self.updated_by_id = user_id

    def toggle_pending(self, user_id: Optional[int] = None) -> bool:
        """
        Toggle pending status.

        Args:
            user_id: ID of user performing the action

        Returns:
            New pending status (True = pending, False = paid)
        """
        self.pending = not self.pending
        if user_id:
            self.updated_by_id = user_id
        return self.pending

    @classmethod
    def get_by_person(cls, person_id: int, include_deleted: bool = False):
        """
        Get all sessions for a person.

        Args:
            person_id: Person's ID
            include_deleted: Whether to include soft-deleted sessions

        Returns:
            Query for sessions
        """
        if include_deleted:
            return cls.query.filter_by(person_id=person_id)
        return cls.query_active().filter_by(person_id=person_id)

    @classmethod
    def get_pending(cls, person_id: Optional[int] = None):
        """
        Get pending sessions.

        Args:
            person_id: Optional person ID to filter by

        Returns:
            Query for pending sessions
        """
        query = cls.query_active().filter_by(pending=True)
        if person_id:
            query = query.filter_by(person_id=person_id)
        return query.order_by(cls.session_date.desc())

    @classmethod
    def get_paid(cls, person_id: Optional[int] = None):
        """
        Get paid sessions.

        Args:
            person_id: Optional person ID to filter by

        Returns:
            Query for paid sessions
        """
        query = cls.query_active().filter_by(pending=False)
        if person_id:
            query = query.filter_by(person_id=person_id)
        return query.order_by(cls.session_date.desc())

    @classmethod
    def calculate_total_pending(cls, person_id: Optional[int] = None) -> float:
        """
        Calculate total pending amount.

        Args:
            person_id: Optional person ID to filter by

        Returns:
            Total pending amount
        """
        query = cls.get_pending(person_id)
        return sum(s.session_price for s in query.all())

    @classmethod
    def create_session(
        cls,
        person_id: int,
        session_date: date,
        session_price: float,
        pending: bool = True,
        created_by_id: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> "TherapySession":
        """
        Create a new therapy session.

        Args:
            person_id: Person's ID
            session_date: Date of the session
            session_price: Price of the session
            pending: Payment status (default True = pending)
            created_by_id: ID of user creating the session
            notes: Optional notes

        Returns:
            New TherapySession instance (not yet committed)
        """
        session = cls(
            person_id=person_id,
            session_date=session_date,
            session_price=session_price,
            pending=pending,
            notes=notes,
            created_by_id=created_by_id,
        )
        return session

    def to_dict(self) -> dict:
        """Convert session to dictionary for API responses."""
        return {
            "id": self.id,
            "person_id": self.person_id,
            "session_date": (
                self.session_date.isoformat() if self.session_date else None
            ),
            "session_price": self.session_price,
            "pending": self.pending,
            "status": self.status_text,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
