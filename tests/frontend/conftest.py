"""
Frontend test fixtures.

Provides Playwright browser and page fixtures for frontend testing.
"""

import os
from datetime import date

import pytest
from playwright.sync_api import sync_playwright

from app import create_app
from app.extensions import db
from app.models.person import Person
from app.models.session import TherapySession
from app.models.user import User


# Screenshots directory
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


@pytest.fixture(scope="session")
def screenshots_dir():
    """Ensure screenshots directory exists."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    return SCREENSHOTS_DIR


@pytest.fixture(scope="session")
def app_config():
    """Application configuration for testing."""
    return {
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for testing
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SERVER_NAME": "localhost:5000",
    }


@pytest.fixture(scope="function")
def live_app(app_config):
    """
    Create application with live server for Playwright tests.
    """
    app = create_app("testing")
    app.config.update(app_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def browser():
    """
    Create a Playwright browser instance.
    
    Runs in headless mode by default. Set PLAYWRIGHT_HEADLESS=0 for headed mode.
    """
    headless = os.environ.get("PLAYWRIGHT_HEADLESS", "1") == "1"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    """Create a new browser context for each test."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="es-ES",
    )
    yield context
    context.close()


@pytest.fixture
def page(context):
    """Create a new page in the browser context."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def auth_user(live_app):
    """Create and return a test user for authentication."""
    with live_app.app_context():
        user = User.create_user(
            email="test@example.com",
            password="test123",
            role="therapist"
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture
def patient(live_app, auth_user):
    """Create a test patient."""
    with live_app.app_context():
        person = Person(
            name="Paciente de Prueba",
            notes="Notas de prueba",
            created_by_id=auth_user.id
        )
        db.session.add(person)
        db.session.commit()
        db.session.refresh(person)
        return person


@pytest.fixture
def pending_session(live_app, patient, auth_user):
    """Create a pending therapy session."""
    with live_app.app_context():
        session = TherapySession(
            person_id=patient.id,
            session_date=date.today(),
            session_price=100.00,
            pending=True,
            created_by_id=auth_user.id
        )
        db.session.add(session)
        db.session.commit()
        db.session.refresh(session)
        return session


@pytest.fixture
def paid_session(live_app, patient, auth_user):
    """Create a paid therapy session."""
    with live_app.app_context():
        session = TherapySession(
            person_id=patient.id,
            session_date=date.today(),
            session_price=150.00,
            pending=False,
            created_by_id=auth_user.id
        )
        db.session.add(session)
        db.session.commit()
        db.session.refresh(session)
        return session


def login(page, base_url, email="test@example.com", password="test123"):
    """
    Helper function to log in a user.
    
    Args:
        page: Playwright page
        base_url: Application base URL
        email: User email
        password: User password
    """
    page.goto(f"{base_url}/auth/login")
    page.fill("input[name='email']", email)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")
    page.wait_for_url(f"{base_url}/patients/")
