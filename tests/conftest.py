"""
Pytest configuration and fixtures.

Provides test fixtures for the entire test suite.
"""

from datetime import date, timedelta

import pytest

from app import create_app
from app.extensions import db
from app.models.person import Person
from app.models.session import TherapySession
from app.models.user import User


@pytest.fixture(scope="function")
def app():
    """
    Create application for testing.

    Uses in-memory SQLite database.
    """
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client for making HTTP requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI test runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User.create_user(email="test@example.com", password="TestPass123", role="therapist")
        db.session.add(user)
        db.session.commit()

        # Refresh to get ID
        db.session.refresh(user)
        return user


@pytest.fixture
def admin_user(app):
    """Create an admin user for testing."""
    with app.app_context():
        user = User.create_user(email="admin@example.com", password="AdminPass123", role="admin")
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture
def sample_person(app, sample_user):
    """Create a sample patient for testing."""
    with app.app_context():
        person = Person(name="Test Patient", notes="Test notes", created_by_id=sample_user.id)
        db.session.add(person)
        db.session.commit()
        db.session.refresh(person)
        return person


@pytest.fixture
def sample_session(app, sample_person, sample_user):
    """Create a sample therapy session for testing."""
    with app.app_context():
        session = TherapySession(
            person_id=sample_person.id,
            session_date=date.today(),
            session_price=100.00,
            pending=True,
            created_by_id=sample_user.id,
        )
        db.session.add(session)
        db.session.commit()
        db.session.refresh(session)
        return session


@pytest.fixture
def multiple_sessions(app, sample_person, sample_user):
    """Create multiple therapy sessions for testing."""
    with app.app_context():
        sessions = []
        for i in range(5):
            session = TherapySession(
                person_id=sample_person.id,
                session_date=date.today() - timedelta(days=i * 7),
                session_price=100.00 + (i * 10),
                pending=(i % 2 == 0),  # Alternate pending/paid
                created_by_id=sample_user.id,
            )
            db.session.add(session)
            sessions.append(session)

        db.session.commit()
        for s in sessions:
            db.session.refresh(s)
        return sessions


class AuthActions:
    """Helper class for authentication in tests."""

    def __init__(self, client):
        self._client = client

    def login(self, email="test@example.com", password="TestPass123"):
        """Log in with credentials."""
        return self._client.post(
            "/auth/login",
            data={"email": email, "password": password},
            follow_redirects=True,
        )

    def logout(self):
        """Log out current user."""
        return self._client.get("/auth/logout", follow_redirects=True)


@pytest.fixture
def auth(client):
    """Authentication helper fixture."""
    return AuthActions(client)


@pytest.fixture
def logged_in_client(client, sample_user, auth):
    """Client that is already logged in."""
    auth.login()
    return client


@pytest.fixture
def logged_in_admin(client, admin_user, auth):
    """Client logged in as admin."""
    auth.login(email="admin@example.com", password="AdminPass123")
    return client
