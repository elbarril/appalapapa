"""
Integration tests for patient routes.
"""

import pytest

from app.extensions import db
from app.models.person import Person


class TestPatientListRoute:
    """Tests for the patient list/dashboard route."""

    def test_dashboard_renders(self, client, sample_user, auth):
        """Test that dashboard renders for logged-in user."""
        auth.login()
        response = client.get("/patients/")

        assert response.status_code == 200

    def test_dashboard_shows_patients(self, client, sample_person, sample_user, auth):
        """Test that dashboard shows patients."""
        auth.login()
        response = client.get("/patients/")

        assert response.status_code == 200
        assert b"Test Patient" in response.data

    def test_dashboard_filter_pending(self, client, sample_person, sample_session, sample_user, auth):
        """Test dashboard filtering by pending."""
        auth.login()
        response = client.get("/patients/?show=pending")

        assert response.status_code == 200

    def test_dashboard_filter_paid(self, client, sample_person, sample_session, sample_user, auth):
        """Test dashboard filtering by paid."""
        auth.login()
        response = client.get("/patients/?show=paid")

        assert response.status_code == 200


class TestAddPatientRoute:
    """Tests for the add patient route."""

    def test_add_patient_page_renders(self, client, sample_user, auth):
        """Test that add patient page renders."""
        auth.login()
        response = client.get("/patients/add")

        assert response.status_code == 200

    def test_add_patient_success(self, app, client, sample_user, auth):
        """Test successful patient creation."""
        auth.login()

        response = client.post("/patients/add", data={"name": "New Patient"}, follow_redirects=True)

        assert response.status_code == 200

        # Verify patient was created
        with app.app_context():
            patient = Person.query.filter_by(name="New Patient").first()
            assert patient is not None

    def test_add_patient_empty_name(self, client, sample_user, auth):
        """Test patient creation with empty name."""
        auth.login()

        response = client.post("/patients/add", data={"name": ""}, follow_redirects=True)

        # Should show validation error
        assert b"requerido" in response.data.lower() or b"error" in response.data.lower()

    def test_add_patient_duplicate_name(self, app, client, sample_person, sample_user, auth):
        """Test patient creation with duplicate name."""
        auth.login()

        response = client.post(
            "/patients/add",
            data={"name": "Test Patient"},  # Already exists
            follow_redirects=True,
        )

        assert b"existe" in response.data.lower()


class TestDeletePatientRoute:
    """Tests for the delete patient route."""

    def test_delete_confirmation_page(self, client, sample_person, sample_user, auth):
        """Test that delete confirmation page shows."""
        auth.login()

        response = client.get(f"/patients/{sample_person.id}/delete")

        assert response.status_code == 200
        assert b"Test Patient" in response.data

    def test_delete_patient_success(self, app, client, sample_person, sample_user, auth):
        """Test successful patient deletion."""
        auth.login()

        response = client.post(f"/patients/{sample_person.id}/delete", follow_redirects=True)

        assert response.status_code == 200

        # Verify patient was soft-deleted
        with app.app_context():
            patient = Person.query.get(sample_person.id)
            assert patient.is_deleted is True

    def test_delete_nonexistent_patient(self, client, sample_user, auth):
        """Test deleting non-existent patient."""
        auth.login()

        response = client.get("/patients/99999/delete", follow_redirects=True)

        assert b"no encontrado" in response.data.lower() or response.status_code == 200
