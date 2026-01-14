"""
Unit tests for form validators.
"""

from datetime import date

import pytest

from app.validators.forms import (
    EditSessionForm,
    LoginForm,
    PersonForm,
    RegistrationForm,
    SessionForm,
)


class TestLoginForm:
    """Tests for the LoginForm."""

    def test_valid_login_data(self, app):
        """Test form with valid data."""
        with app.app_context():
            form = LoginForm(data={"email": "test@example.com", "password": "password123"})

            assert form.validate() is True

    def test_missing_email(self, app):
        """Test form with missing email."""
        with app.app_context():
            form = LoginForm(data={"password": "password123"})

            assert form.validate() is False
            assert "email" in form.errors

    def test_invalid_email_format(self, app):
        """Test form with invalid email format."""
        with app.app_context():
            form = LoginForm(data={"email": "not-an-email", "password": "password123"})

            assert form.validate() is False
            assert "email" in form.errors

    def test_missing_password(self, app):
        """Test form with missing password."""
        with app.app_context():
            form = LoginForm(data={"email": "test@example.com"})

            assert form.validate() is False
            assert "password" in form.errors


class TestRegistrationForm:
    """Tests for the RegistrationForm."""

    def test_valid_registration_data(self, app):
        """Test form with valid data."""
        with app.app_context():
            form = RegistrationForm(
                data={
                    "email": "new@example.com",
                    "password": "SecurePass1",
                    "confirm_password": "SecurePass1",
                }
            )

            assert form.validate() is True

    def test_password_mismatch(self, app):
        """Test form with mismatched passwords."""
        with app.app_context():
            form = RegistrationForm(
                data={
                    "email": "new@example.com",
                    "password": "SecurePass1",
                    "confirm_password": "DifferentPass1",
                }
            )

            assert form.validate() is False
            assert "confirm_password" in form.errors

    def test_password_too_short(self, app):
        """Test form with password too short."""
        with app.app_context():
            form = RegistrationForm(
                data={
                    "email": "new@example.com",
                    "password": "short",
                    "confirm_password": "short",
                }
            )

            assert form.validate() is False
            assert "password" in form.errors

    def test_password_without_number(self, app):
        """Test form with password without numbers."""
        with app.app_context():
            form = RegistrationForm(
                data={
                    "email": "new@example.com",
                    "password": "NoNumbersHere",
                    "confirm_password": "NoNumbersHere",
                }
            )

            assert form.validate() is False
            assert "password" in form.errors


class TestPersonForm:
    """Tests for the PersonForm."""

    def test_valid_person_data(self, app):
        """Test form with valid data."""
        with app.app_context():
            form = PersonForm(data={"name": "John Doe"})

            assert form.validate() is True

    def test_missing_name(self, app):
        """Test form with missing name."""
        with app.app_context():
            form = PersonForm(data={})

            assert form.validate() is False
            assert "name" in form.errors

    def test_name_too_short(self, app):
        """Test form with name too short."""
        with app.app_context():
            form = PersonForm(data={"name": "X"})

            assert form.validate() is False
            assert "name" in form.errors

    def test_name_with_notes(self, app):
        """Test form with optional notes."""
        with app.app_context():
            form = PersonForm(data={"name": "John Doe", "notes": "Some notes about the patient"})

            assert form.validate() is True


class TestSessionForm:
    """Tests for the SessionForm."""

    def test_valid_session_data(self, app):
        """Test form with valid data."""
        with app.app_context():
            form = SessionForm(
                data={
                    "person_id": 1,
                    "session_date": date.today(),
                    "session_price": 100.00,
                }
            )
            form.person_id.choices = [(1, "Test Patient")]

            assert form.validate() is True

    def test_missing_person_id(self, app):
        """Test form with missing patient."""
        with app.app_context():
            form = SessionForm(data={"session_date": date.today(), "session_price": 100.00})
            # Need to set choices before validating SelectField
            form.person_id.choices = [(1, "Test Patient")]

            assert form.validate() is False
            assert "person_id" in form.errors

    def test_negative_price(self, app):
        """Test form with negative price."""
        with app.app_context():
            form = SessionForm(
                data={
                    "person_id": 1,
                    "session_date": date.today(),
                    "session_price": -50.00,
                }
            )
            form.person_id.choices = [(1, "Test Patient")]

            assert form.validate() is False
            assert "session_price" in form.errors

    def test_price_too_high(self, app):
        """Test form with price exceeding maximum."""
        with app.app_context():
            form = SessionForm(
                data={
                    "person_id": 1,
                    "session_date": date.today(),
                    "session_price": 2000000.00,  # Over MAX_PRICE
                }
            )
            form.person_id.choices = [(1, "Test Patient")]

            assert form.validate() is False
            assert "session_price" in form.errors


class TestEditSessionForm:
    """Tests for the EditSessionForm."""

    def test_valid_edit_data(self, app):
        """Test form with valid data."""
        with app.app_context():
            form = EditSessionForm(data={"session_date": date.today(), "session_price": 150.00})

            assert form.validate() is True

    def test_missing_date(self, app):
        """Test form with missing date."""
        with app.app_context():
            form = EditSessionForm(data={"session_price": 150.00})

            assert form.validate() is False
            assert "session_date" in form.errors

    def test_missing_price(self, app):
        """Test form with missing price."""
        with app.app_context():
            form = EditSessionForm(data={"session_date": date.today()})

            assert form.validate() is False
            assert "session_price" in form.errors
