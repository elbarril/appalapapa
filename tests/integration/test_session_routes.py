"""
Integration tests for session routes.
"""
import pytest
from datetime import date, timedelta

from app.models.session import TherapySession
from app.extensions import db


class TestAddSessionRoute:
    """Tests for the add session route."""
    
    def test_add_session_page_renders(self, client, sample_person, sample_user, auth):
        """Test that add session page renders."""
        auth.login()
        response = client.get('/sessions/add')
        
        assert response.status_code == 200
    
    def test_add_session_success(self, app, client, sample_person, sample_user, auth):
        """Test successful session creation."""
        auth.login()
        
        response = client.post('/sessions/add', data={
            'person_id': sample_person.id,
            'session_date': date.today().strftime('%Y-%m-%d'),
            'session_price': '150.00'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify session was created
        with app.app_context():
            session = TherapySession.query.filter_by(
                person_id=sample_person.id,
                session_price=150.00
            ).first()
            assert session is not None
    
    def test_add_session_no_patients_redirect(self, app, client, sample_user, auth):
        """Test redirect when no patients exist."""
        with app.app_context():
            # Delete all patients first
            from app.models.person import Person
            Person.query.delete()
            db.session.commit()
        
        auth.login()
        response = client.get('/sessions/add', follow_redirects=True)
        
        # Should redirect to add patient or show warning
        assert response.status_code == 200


class TestEditSessionRoute:
    """Tests for the edit session route."""
    
    def test_edit_session_page_renders(self, client, sample_person, sample_session, sample_user, auth):
        """Test that edit session page renders."""
        auth.login()
        
        response = client.get(f'/sessions/{sample_person.id}/{sample_session.id}/edit')
        
        assert response.status_code == 200
    
    def test_edit_session_success(self, app, client, sample_person, sample_session, sample_user, auth):
        """Test successful session update."""
        auth.login()
        
        new_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        response = client.post(
            f'/sessions/{sample_person.id}/{sample_session.id}/edit',
            data={
                'session_date': new_date,
                'session_price': '200.00'
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200
        
        # Verify session was updated
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)
            assert session.session_price == 200.00
    
    def test_edit_nonexistent_session(self, client, sample_person, sample_user, auth):
        """Test editing non-existent session."""
        auth.login()
        
        response = client.get(
            f'/sessions/{sample_person.id}/99999/edit',
            follow_redirects=True
        )
        
        assert b'no encontrada' in response.data.lower() or response.status_code == 200


class TestDeleteSessionRoute:
    """Tests for the delete session route."""
    
    def test_delete_session_success(self, app, client, sample_session, sample_user, auth):
        """Test successful session deletion."""
        auth.login()
        
        response = client.get(
            f'/sessions/{sample_session.id}/remove',
            follow_redirects=True
        )
        
        assert response.status_code == 200
        
        # Verify session was soft-deleted
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)
            assert session.is_deleted is True
    
    def test_delete_nonexistent_session(self, client, sample_user, auth):
        """Test deleting non-existent session."""
        auth.login()
        
        response = client.get('/sessions/99999/remove', follow_redirects=True)
        
        # Should show error but not crash
        assert response.status_code == 200


class TestTogglePaymentRoute:
    """Tests for the toggle payment status route."""
    
    def test_toggle_pending_to_paid(self, app, client, sample_session, sample_user, auth):
        """Test toggling from pending to paid."""
        auth.login()
        
        response = client.get(
            f'/sessions/{sample_session.id}/toggle',
            follow_redirects=True
        )
        
        assert response.status_code == 200
        
        # Verify status changed
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)
            assert session.pending is False
    
    def test_toggle_paid_to_pending(self, app, client, sample_session, sample_user, auth):
        """Test toggling from paid to pending."""
        # First set to paid
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)
            session.pending = False
            db.session.commit()
        
        auth.login()
        
        response = client.get(
            f'/sessions/{sample_session.id}/toggle',
            follow_redirects=True
        )
        
        assert response.status_code == 200
        
        # Verify status changed back
        with app.app_context():
            session = TherapySession.query.get(sample_session.id)
            assert session.pending is True
