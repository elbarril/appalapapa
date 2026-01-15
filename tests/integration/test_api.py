"""
Integration tests for REST API v1 endpoints.

Tests all API endpoints for patients and sessions.
"""

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.person import Person
from app.models.session import TherapySession


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns ok."""
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert data["version"] == "v1"


class TestPatientsAPI:
    """Tests for the patients API endpoints."""

    def test_list_patients_requires_auth(self, client):
        """Test that listing patients requires authentication."""
        response = client.get("/api/v1/patients")

        # Should redirect to login or return 401
        assert response.status_code in [302, 401]

    def test_list_patients_success(self, client, sample_person, sample_user, auth):
        """Test listing patients when authenticated."""
        auth.login()
        response = client.get("/api/v1/patients")

        assert response.status_code == 200
        data = response.get_json()
        assert "patients" in data
        assert "count" in data
        assert data["count"] >= 1

    def test_get_patient_success(self, client, sample_person, sample_user, auth):
        """Test getting a single patient."""
        auth.login()
        response = client.get(f"/api/v1/patients/{sample_person.id}")

        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == sample_person.id
        assert data["name"] == sample_person.name

    def test_get_patient_not_found(self, client, sample_user, auth):
        """Test getting a non-existent patient."""
        auth.login()
        response = client.get("/api/v1/patients/99999")

        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_create_patient_success(self, app, client, sample_user, auth):
        """Test creating a new patient via API."""
        auth.login()
        response = client.post(
            "/api/v1/patients",
            json={"name": "API Patient", "notes": "Created via API"},
            content_type="application/json",
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "API Patient"
        assert data["notes"] == "Created via API"

        # Verify in database
        with app.app_context():
            patient = Person.query.filter_by(name="API Patient").first()
            assert patient is not None

    def test_create_patient_missing_name(self, client, sample_user, auth):
        """Test creating patient without name fails."""
        auth.login()
        response = client.post(
            "/api/v1/patients",
            json={"notes": "No name provided"},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_patient_duplicate_name(self, client, sample_person, sample_user, auth):
        """Test creating patient with duplicate name fails."""
        auth.login()
        response = client.post(
            "/api/v1/patients",
            json={"name": sample_person.name},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_update_patient_success(self, app, client, sample_person, sample_user, auth):
        """Test updating a patient via API."""
        auth.login()
        response = client.put(
            f"/api/v1/patients/{sample_person.id}",
            json={"name": "Updated Patient Name", "notes": "Updated notes"},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Updated Patient Name"
        assert data["notes"] == "Updated notes"

        # Verify in database
        with app.app_context():
            patient = Person.query.get(sample_person.id)
            assert patient.name == "Updated Patient Name"

    def test_update_patient_not_found(self, client, sample_user, auth):
        """Test updating non-existent patient fails."""
        auth.login()
        response = client.put(
            "/api/v1/patients/99999",
            json={"name": "New Name"},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_update_patient_missing_name(self, client, sample_person, sample_user, auth):
        """Test updating patient without name fails."""
        auth.login()
        response = client.put(
            f"/api/v1/patients/{sample_person.id}",
            json={"notes": "Only notes"},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_delete_patient_success(self, app, client, sample_person, sample_user, auth):
        """Test deleting a patient via API (soft delete)."""
        auth.login()
        response = client.delete(f"/api/v1/patients/{sample_person.id}")

        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data

        # Verify soft-deleted in database
        with app.app_context():
            patient = Person.query.get(sample_person.id)
            assert patient.is_deleted is True

    def test_delete_patient_not_found(self, client, sample_user, auth):
        """Test deleting non-existent patient fails."""
        auth.login()
        response = client.delete("/api/v1/patients/99999")

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestSessionsAPI:
    """Tests for the sessions API endpoints."""

    def test_list_sessions_success(self, client, sample_person, sample_session, sample_user, auth):
        """Test listing sessions for a patient."""
        auth.login()
        response = client.get(f"/api/v1/patients/{sample_person.id}/sessions")

        assert response.status_code == 200
        data = response.get_json()
        assert "sessions" in data
        assert "count" in data
        assert data["count"] >= 1

    def test_get_session_success(self, client, sample_session, sample_user, auth):
        """Test getting a single session."""
        auth.login()
        response = client.get(f"/api/v1/sessions/{sample_session.id}")

        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == sample_session.id
        assert data["session_price"] == sample_session.session_price

    def test_get_session_not_found(self, client, sample_user, auth):
        """Test getting a non-existent session."""
        auth.login()
        response = client.get("/api/v1/sessions/99999")

        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_create_session_success(self, app, client, sample_person, sample_user, auth):
        """Test creating a new session via API."""
        auth.login()
        response = client.post(
            "/api/v1/sessions",
            json={
                "person_id": sample_person.id,
                "session_date": date.today().isoformat(),
                "session_price": 150.00,
                "pending": True,
            },
            content_type="application/json",
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["session_price"] == 150.00
        assert data["pending"] is True

        # Verify in database
        with app.app_context():
            session = TherapySession.query.filter_by(session_price=150.00).first()
            assert session is not None

    def test_create_session_missing_fields(self, client, sample_person, sample_user, auth):
        """Test creating session without required fields fails."""
        auth.login()
        response = client.post(
            "/api/v1/sessions",
            json={"person_id": sample_person.id},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_session_invalid_date_format(self, client, sample_person, sample_user, auth):
        """Test creating session with invalid date format fails."""
        auth.login()
        response = client.post(
            "/api/v1/sessions",
            json={
                "person_id": sample_person.id,
                "session_date": "invalid-date",
                "session_price": 100.00,
            },
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_update_session_success(self, app, client, sample_session, sample_user, auth):
        """Test updating a session via API."""
        auth.login()
        new_date = (date.today() - timedelta(days=1)).isoformat()
        response = client.put(
            f"/api/v1/sessions/{sample_session.id}",
            json={
                "session_date": new_date,
                "session_price": 200.00,
                "pending": False,
                "notes": "Updated via API",
            },
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["session_price"] == 200.00
        assert data["pending"] is False

        # Verify in database
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)
            assert session.session_price == 200.00
            assert session.pending is False

    def test_update_session_not_found(self, client, sample_user, auth):
        """Test updating non-existent session fails."""
        auth.login()
        response = client.put(
            "/api/v1/sessions/99999",
            json={
                "session_date": date.today().isoformat(),
                "session_price": 100.00,
            },
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_update_session_missing_fields(self, client, sample_session, sample_user, auth):
        """Test updating session without required fields fails."""
        auth.login()
        response = client.put(
            f"/api/v1/sessions/{sample_session.id}",
            json={"notes": "Only notes"},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_delete_session_success(self, app, client, sample_session, sample_user, auth):
        """Test deleting a session via API (soft delete)."""
        auth.login()
        response = client.delete(f"/api/v1/sessions/{sample_session.id}")

        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data

        # Verify soft-deleted in database
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)
            assert session.is_deleted is True

    def test_delete_session_not_found(self, client, sample_user, auth):
        """Test deleting non-existent session fails."""
        auth.login()
        response = client.delete("/api/v1/sessions/99999")

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_toggle_session_payment_success(self, app, client, sample_session, sample_user, auth):
        """Test toggling session payment status via API."""
        auth.login()
        
        # Initial state is pending=True
        response = client.post(f"/api/v1/sessions/{sample_session.id}/toggle")

        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert "pending" in data
        assert data["pending"] is False  # Toggled from True to False

        # Toggle again
        response = client.post(f"/api/v1/sessions/{sample_session.id}/toggle")

        assert response.status_code == 200
        data = response.get_json()
        assert data["pending"] is True  # Toggled back to True

    def test_toggle_session_not_found(self, client, sample_user, auth):
        """Test toggling non-existent session fails."""
        auth.login()
        response = client.post("/api/v1/sessions/99999/toggle")

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestStatsAPI:
    """Tests for the statistics API endpoint."""

    def test_get_stats_success(self, client, sample_person, sample_session, sample_user, auth):
        """Test getting statistics."""
        auth.login()
        response = client.get("/api/v1/stats")

        assert response.status_code == 200
        data = response.get_json()
        assert "patients_count" in data
        assert "pending_total" in data
        assert "paid_total" in data
        assert "grand_total" in data

    def test_get_stats_requires_auth(self, client):
        """Test that stats endpoint requires authentication."""
        response = client.get("/api/v1/stats")

        assert response.status_code in [302, 401]


class TestDashboardAPI:
    """Tests for the dashboard API endpoint."""

    def test_get_dashboard_success(self, client, sample_person, sample_session, sample_user, auth):
        """Test getting dashboard data."""
        auth.login()
        response = client.get("/api/v1/dashboard")

        assert response.status_code == 200
        data = response.get_json()
        assert "grouped_sessions" in data
        assert "total" in data
        assert "current_filter" in data
        assert "filters" in data
        assert "allow_delete" in data
        assert data["current_filter"] == "all"
        assert len(data["filters"]) == 3

    def test_get_dashboard_with_filter(self, client, sample_person, sample_session, sample_user, auth):
        """Test getting dashboard data with pending filter."""
        auth.login()
        response = client.get("/api/v1/dashboard?show=pending")

        assert response.status_code == 200
        data = response.get_json()
        assert data["current_filter"] == "pending"
        # Sample session is pending by default
        assert data["total"] >= 1

    def test_get_dashboard_paid_filter(self, client, sample_person, sample_user, auth, app):
        """Test getting dashboard data with paid filter."""
        # Create a paid session directly
        from app.models.session import TherapySession
        from datetime import date

        with app.app_context():
            paid_session = TherapySession(
                person_id=sample_person.id,
                session_date=date.today(),
                session_price=100.00,
                pending=False,  # Paid
                created_by_id=sample_user.id,
            )
            db.session.add(paid_session)
            db.session.commit()

        auth.login()
        response = client.get("/api/v1/dashboard?show=paid")

        assert response.status_code == 200
        data = response.get_json()
        assert data["current_filter"] == "paid"
        assert data["total"] >= 1

    def test_get_dashboard_requires_auth(self, client):
        """Test that dashboard endpoint requires authentication."""
        response = client.get("/api/v1/dashboard")

        assert response.status_code in [302, 401]
