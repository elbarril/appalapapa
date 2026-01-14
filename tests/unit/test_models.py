"""
Unit tests for database models.
"""

import pytest
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.user import User
from app.models.person import Person
from app.models.session import TherapySession
from app.utils.constants import UserRole


class TestUserModel:
    """Tests for the User model."""

    def test_create_user(self, app):
        """Test creating a new user."""
        with app.app_context():
            user = User.create_user("new@example.com", "password123")
            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.email == "new@example.com"
            assert user.is_active is True

    def test_password_hashing(self, app):
        """Test password is properly hashed and verifiable."""
        with app.app_context():
            user = User(email="test@example.com")
            user.set_password("SecurePass123")

            # Password should be hashed, not stored as plaintext
            assert user.password_hash != "SecurePass123"

            # Correct password should verify
            assert user.check_password("SecurePass123") is True

            # Wrong password should not verify
            assert user.check_password("WrongPassword") is False

    def test_email_uniqueness(self, app, sample_user):
        """Test that duplicate emails raise an error."""
        with app.app_context():
            duplicate = User(email="test@example.com")
            duplicate.set_password("password")
            db.session.add(duplicate)

            with pytest.raises(IntegrityError):
                db.session.commit()

    def test_get_by_email(self, app, sample_user):
        """Test finding user by email."""
        with app.app_context():
            found = User.get_by_email("test@example.com")
            assert found is not None
            assert found.email == "test@example.com"

            not_found = User.get_by_email("nonexistent@example.com")
            assert not_found is None

    def test_user_roles(self, app):
        """Test user role checking."""
        with app.app_context():
            admin = User.create_user("admin@example.com", "pass", UserRole.ADMIN)
            therapist = User.create_user(
                "therapist@example.com", "pass", UserRole.THERAPIST
            )
            viewer = User.create_user("viewer@example.com", "pass", UserRole.VIEWER)

            assert admin.is_admin is True
            assert admin.is_therapist is False

            assert therapist.is_therapist is True
            assert therapist.is_admin is False

            assert viewer.is_viewer is True
            assert viewer.has_role(UserRole.VIEWER) is True

    def test_has_any_role(self, app):
        """Test checking multiple roles."""
        with app.app_context():
            admin = User.create_user("admin@example.com", "pass", UserRole.ADMIN)

            assert admin.has_any_role(UserRole.ADMIN, UserRole.THERAPIST) is True
            assert admin.has_any_role(UserRole.THERAPIST, UserRole.VIEWER) is False

    def test_update_last_login(self, app):
        """Test updating last login timestamp."""
        with app.app_context():
            user = User.create_user("test@example.com", "pass")
            assert user.last_login_at is None

            user.update_last_login()
            assert user.last_login_at is not None
            assert (datetime.utcnow() - user.last_login_at).seconds < 5


class TestPersonModel:
    """Tests for the Person (Patient) model."""

    def test_create_person(self, app):
        """Test creating a new patient."""
        with app.app_context():
            person = Person(name="John Doe")
            db.session.add(person)
            db.session.commit()

            assert person.id is not None
            assert person.name == "John Doe"
            assert person.is_active is True

    def test_name_uniqueness(self, app, sample_person):
        """Test that duplicate names raise an error."""
        with app.app_context():
            duplicate = Person(name="Test Patient")
            db.session.add(duplicate)

            with pytest.raises(IntegrityError):
                db.session.commit()

    def test_soft_delete(self, app, sample_person):
        """Test soft delete functionality."""
        with app.app_context():
            person = Person.query.get(sample_person.id)

            assert person.is_deleted is False

            person.soft_delete(user_id=1)
            db.session.commit()

            assert person.is_deleted is True
            assert person.deleted_at is not None

            # Should not appear in active query
            active = Person.query_active().filter_by(id=sample_person.id).first()
            assert active is None

    def test_restore(self, app, sample_person):
        """Test restoring a soft-deleted patient."""
        with app.app_context():
            person = Person.query.get(sample_person.id)
            person.soft_delete()
            db.session.commit()

            person.restore()
            db.session.commit()

            assert person.is_deleted is False
            assert person.deleted_at is None

    def test_session_count(self, app, sample_person, multiple_sessions):
        """Test session count property."""
        with app.app_context():
            person = Person.query.get(sample_person.id)
            assert person.session_count == 5

    def test_pending_total(self, app, sample_person, multiple_sessions):
        """Test pending total calculation."""
        with app.app_context():
            person = Person.query.get(sample_person.id)
            # Sessions 0, 2, 4 are pending (i % 2 == 0)
            # Prices: 100, 120, 140
            expected = 100 + 120 + 140
            assert person.pending_total == expected

    def test_to_dict(self, app, sample_person):
        """Test dictionary serialization."""
        with app.app_context():
            person = Person.query.get(sample_person.id)
            data = person.to_dict()

            assert "id" in data
            assert "name" in data
            assert data["name"] == "Test Patient"
            assert "session_count" in data


class TestTherapySessionModel:
    """Tests for the TherapySession model."""

    def test_create_session(self, app, sample_person):
        """Test creating a new therapy session."""
        with app.app_context():
            session = TherapySession(
                person_id=sample_person.id,
                session_date=date.today(),
                session_price=150.00,
                pending=True,
            )
            db.session.add(session)
            db.session.commit()

            assert session.id is not None
            assert session.session_price == 150.00
            assert session.is_pending is True

    def test_toggle_pending(self, app, sample_session):
        """Test toggling payment status."""
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)

            assert session.pending is True

            new_status = session.toggle_pending()
            assert new_status is False
            assert session.pending is False

            new_status = session.toggle_pending()
            assert new_status is True
            assert session.pending is True

    def test_mark_as_paid(self, app, sample_session):
        """Test marking session as paid."""
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)

            session.mark_as_paid()
            assert session.is_paid is True
            assert session.is_pending is False

    def test_cascade_delete(self, app, sample_person, sample_session):
        """Test that deleting person cascades to sessions."""
        with app.app_context():
            person = Person.query.get(sample_person.id)
            session_id = sample_session.id

            db.session.delete(person)
            db.session.commit()

            # Session should be deleted too
            session = TherapySession.query.get(session_id)
            assert session is None

    def test_get_pending(self, app, sample_person, multiple_sessions):
        """Test querying pending sessions."""
        with app.app_context():
            pending = TherapySession.get_pending(sample_person.id).all()

            # 3 sessions are pending (indices 0, 2, 4)
            assert len(pending) == 3
            for session in pending:
                assert session.pending is True

    def test_get_paid(self, app, sample_person, multiple_sessions):
        """Test querying paid sessions."""
        with app.app_context():
            paid = TherapySession.get_paid(sample_person.id).all()

            # 2 sessions are paid (indices 1, 3)
            assert len(paid) == 2
            for session in paid:
                assert session.pending is False

    def test_calculate_total_pending(self, app, sample_person, multiple_sessions):
        """Test calculating total pending amount."""
        with app.app_context():
            total = TherapySession.calculate_total_pending(sample_person.id)

            # Pending sessions: 100, 120, 140
            expected = 100 + 120 + 140
            assert total == expected

    def test_status_text(self, app, sample_session):
        """Test status text property."""
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)

            assert session.status_text == "Pendiente"

            session.mark_as_paid()
            assert session.status_text == "Pagado"

    def test_to_dict(self, app, sample_session):
        """Test dictionary serialization."""
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)
            data = session.to_dict()

            assert "id" in data
            assert "session_date" in data
            assert "session_price" in data
            assert "pending" in data
            assert "status" in data
