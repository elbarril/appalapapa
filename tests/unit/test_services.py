"""
Unit tests for service layer.
"""
import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

from app.extensions import db
from app.models.user import User
from app.models.person import Person
from app.models.session import TherapySession
from app.services.auth_service import AuthService
from app.services.patient_service import PatientService
from app.services.session_service import SessionService


class TestAuthService:
    """Tests for the AuthService."""
    
    def test_authenticate_success(self, app, sample_user):
        """Test successful authentication."""
        with app.app_context():
            success, user, message = AuthService.authenticate(
                'test@example.com',
                'TestPass123'
            )
            
            assert success is True
            assert user is not None
            assert user.email == 'test@example.com'
    
    def test_authenticate_wrong_password(self, app, sample_user):
        """Test authentication with wrong password."""
        with app.app_context():
            success, user, message = AuthService.authenticate(
                'test@example.com',
                'WrongPassword'
            )
            
            assert success is False
            assert user is None
            assert 'incorrecto' in message.lower()
    
    def test_authenticate_nonexistent_user(self, app):
        """Test authentication with non-existent email."""
        with app.app_context():
            success, user, message = AuthService.authenticate(
                'nonexistent@example.com',
                'password'
            )
            
            assert success is False
            assert user is None
    
    def test_authenticate_inactive_user(self, app, sample_user):
        """Test authentication with inactive user."""
        with app.app_context():
            user = User.query.get(sample_user.id)
            user.is_active = False
            db.session.commit()
            
            success, _, message = AuthService.authenticate(
                'test@example.com',
                'TestPass123'
            )
            
            assert success is False
            assert 'desactivada' in message.lower()
    
    def test_register_success(self, app):
        """Test successful registration."""
        with app.app_context():
            # Set allowed emails in config
            app.config['ALLOWED_EMAILS'] = {'new@example.com'}
            
            success, user, message = AuthService.register(
                'new@example.com',
                'NewPass123'
            )
            
            assert success is True
            assert user is not None
            assert user.email == 'new@example.com'
    
    def test_register_unauthorized_email(self, app):
        """Test registration with unauthorized email."""
        with app.app_context():
            app.config['ALLOWED_EMAILS'] = {'allowed@example.com'}
            
            success, user, message = AuthService.register(
                'unauthorized@example.com',
                'password'
            )
            
            assert success is False
            assert 'autorizado' in message.lower()
    
    def test_register_duplicate_email(self, app, sample_user):
        """Test registration with existing email."""
        with app.app_context():
            app.config['ALLOWED_EMAILS'] = set()  # Allow all
            
            success, user, message = AuthService.register(
                'test@example.com',  # Already exists
                'password'
            )
            
            assert success is False
            assert 'registrado' in message.lower()
    
    def test_change_password_success(self, app, sample_user):
        """Test successful password change."""
        with app.app_context():
            user = User.query.get(sample_user.id)
            
            success, message = AuthService.change_password(
                user,
                'TestPass123',
                'NewPass456'
            )
            
            assert success is True
            assert user.check_password('NewPass456') is True
    
    def test_change_password_wrong_current(self, app, sample_user):
        """Test password change with wrong current password."""
        with app.app_context():
            user = User.query.get(sample_user.id)
            
            success, message = AuthService.change_password(
                user,
                'WrongPassword',
                'NewPass456'
            )
            
            assert success is False
            assert 'incorrecta' in message.lower()


class TestPatientService:
    """Tests for the PatientService."""
    
    def test_create_patient_success(self, app, sample_user):
        """Test successful patient creation."""
        with app.app_context():
            success, person, message = PatientService.create(
                name='New Patient',
                user_id=sample_user.id
            )
            
            assert success is True
            assert person is not None
            assert person.name == 'New Patient'
    
    def test_create_patient_empty_name(self, app):
        """Test patient creation with empty name."""
        with app.app_context():
            success, person, message = PatientService.create(name='')
            
            assert success is False
            assert 'requerido' in message.lower()
    
    def test_create_patient_duplicate(self, app, sample_person):
        """Test patient creation with duplicate name."""
        with app.app_context():
            success, person, message = PatientService.create(
                name='Test Patient'
            )
            
            assert success is False
            assert 'existe' in message.lower()
    
    def test_get_by_id(self, app, sample_person):
        """Test getting patient by ID."""
        with app.app_context():
            person = PatientService.get_by_id(sample_person.id)
            
            assert person is not None
            assert person.name == 'Test Patient'
    
    def test_get_by_id_not_found(self, app):
        """Test getting non-existent patient."""
        with app.app_context():
            person = PatientService.get_by_id(99999)
            
            assert person is None
    
    def test_update_patient_success(self, app, sample_person, sample_user):
        """Test successful patient update."""
        with app.app_context():
            success, person, message = PatientService.update(
                person_id=sample_person.id,
                name='Updated Name',
                user_id=sample_user.id
            )
            
            assert success is True
            assert person.name == 'Updated Name'
    
    def test_delete_patient_soft(self, app, sample_person, sample_user):
        """Test soft deleting a patient."""
        with app.app_context():
            success, message = PatientService.delete(
                person_id=sample_person.id,
                user_id=sample_user.id,
                soft=True
            )
            
            assert success is True
            
            # Should not be in active query
            person = PatientService.get_by_id(sample_person.id)
            assert person is None
            
            # But should still exist in database
            person = Person.query.get(sample_person.id)
            assert person is not None
            assert person.is_deleted is True
    
    def test_get_for_select(self, app, sample_person):
        """Test getting patients for dropdown."""
        with app.app_context():
            choices = PatientService.get_for_select()
            
            assert len(choices) >= 1
            assert any(c[1] == 'Test Patient' for c in choices)


class TestSessionService:
    """Tests for the SessionService."""
    
    def test_create_session_success(self, app, sample_person, sample_user):
        """Test successful session creation."""
        with app.app_context():
            success, session, message = SessionService.create(
                person_id=sample_person.id,
                session_date=date.today(),
                session_price=150.00,
                user_id=sample_user.id
            )
            
            assert success is True
            assert session is not None
            assert session.session_price == 150.00
    
    def test_create_session_negative_price(self, app, sample_person):
        """Test session creation with negative price."""
        with app.app_context():
            success, session, message = SessionService.create(
                person_id=sample_person.id,
                session_date=date.today(),
                session_price=-100.00
            )
            
            assert success is False
            assert 'mayor a cero' in message.lower()
    
    def test_create_session_zero_price(self, app, sample_person):
        """Test session creation with zero price."""
        with app.app_context():
            success, session, message = SessionService.create(
                person_id=sample_person.id,
                session_date=date.today(),
                session_price=0
            )
            
            assert success is False
    
    def test_create_session_far_future_date(self, app, sample_person):
        """Test session creation with date too far in future."""
        with app.app_context():
            future_date = date.today() + timedelta(days=30)
            
            success, session, message = SessionService.create(
                person_id=sample_person.id,
                session_date=future_date,
                session_price=100.00
            )
            
            assert success is False
            assert 'anticipación' in message.lower()
    
    def test_create_session_invalid_person(self, app):
        """Test session creation with non-existent patient."""
        with app.app_context():
            success, session, message = SessionService.create(
                person_id=99999,
                session_date=date.today(),
                session_price=100.00
            )
            
            assert success is False
            assert 'no encontrado' in message.lower()
    
    def test_update_session_success(self, app, sample_session, sample_user):
        """Test successful session update."""
        with app.app_context():
            new_date = date.today() - timedelta(days=1)
            
            success, session, message = SessionService.update(
                session_id=sample_session.id,
                session_date=new_date,
                session_price=200.00,
                user_id=sample_user.id
            )
            
            assert success is True
            assert session.session_price == 200.00
    
    def test_toggle_payment_status(self, app, sample_session, sample_user):
        """Test toggling payment status."""
        with app.app_context():
            # Initially pending
            success, new_status, message = SessionService.toggle_payment_status(
                session_id=sample_session.id,
                user_id=sample_user.id
            )
            
            assert success is True
            assert new_status is False  # Now paid
            
            # Toggle again
            success, new_status, message = SessionService.toggle_payment_status(
                session_id=sample_session.id,
                user_id=sample_user.id
            )
            
            assert success is True
            assert new_status is True  # Now pending again
    
    def test_delete_session_soft(self, app, sample_session, sample_user):
        """Test soft deleting a session."""
        with app.app_context():
            success, message = SessionService.delete(
                session_id=sample_session.id,
                user_id=sample_user.id,
                soft=True
            )
            
            assert success is True
            
            # Should not be in active query
            session = SessionService.get_by_id(sample_session.id)
            assert session is None
    
    def test_calculate_totals(self, app, sample_person, multiple_sessions):
        """Test calculating payment totals."""
        with app.app_context():
            totals = SessionService.calculate_totals(sample_person.id)
            
            assert 'pending_total' in totals
            assert 'paid_total' in totals
            assert 'grand_total' in totals
            
            # Pending: 100 + 120 + 140 = 360
            assert totals['pending_total'] == 360
            
            # Paid: 110 + 130 = 240
            assert totals['paid_total'] == 240
            
            # Total: 600
            assert totals['grand_total'] == 600
