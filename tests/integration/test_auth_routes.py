"""
Integration tests for authentication routes.
"""
import pytest
from flask import url_for

from app.models.user import User
from app.extensions import db


class TestLoginRoute:
    """Tests for the login route."""
    
    def test_login_page_renders(self, client):
        """Test that login page renders correctly."""
        response = client.get('/auth/login')
        
        assert response.status_code == 200
        assert b'Email' in response.data or b'email' in response.data
    
    def test_login_success(self, client, sample_user, auth):
        """Test successful login."""
        response = auth.login()
        
        assert response.status_code == 200
        # Should be redirected to index and see success message
        assert b'correctamente' in response.data.lower() or response.status_code == 200
    
    def test_login_wrong_password(self, client, sample_user):
        """Test login with wrong password."""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'incorrecto' in response.data.lower()
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email."""
        response = client.post('/auth/login', data={
            'email': 'nobody@example.com',
            'password': 'anypassword'
        }, follow_redirects=True)
        
        assert b'incorrecto' in response.data.lower()
    
    def test_login_redirects_when_authenticated(self, client, sample_user, auth):
        """Test that authenticated users are redirected from login page."""
        auth.login()
        
        response = client.get('/auth/login', follow_redirects=False)
        
        assert response.status_code == 302  # Redirect


class TestLogoutRoute:
    """Tests for the logout route."""
    
    def test_logout(self, client, sample_user, auth):
        """Test successful logout."""
        auth.login()
        response = auth.logout()
        
        assert response.status_code == 200
        assert b'cerrada' in response.data.lower() or b'login' in response.data.lower()
    
    def test_logout_redirects_to_login(self, client, sample_user, auth):
        """Test that logout redirects to login page."""
        auth.login()
        
        response = client.get('/auth/logout', follow_redirects=False)
        
        assert response.status_code == 302
        assert '/auth/login' in response.location or 'login' in response.location


class TestRegisterRoute:
    """Tests for the registration route."""
    
    def test_register_page_renders(self, client):
        """Test that register page renders correctly."""
        response = client.get('/auth/register')
        
        assert response.status_code == 200
    
    def test_register_success(self, app, client):
        """Test successful registration."""
        with app.app_context():
            app.config['ALLOWED_EMAILS'] = {'new@example.com'}
            
            response = client.post('/auth/register', data={
                'email': 'new@example.com',
                'password': 'SecurePass1',
                'confirm_password': 'SecurePass1'
            }, follow_redirects=True)
            
            # Should redirect to login with success message
            assert b'xito' in response.data or response.status_code == 200
    
    def test_register_unauthorized_email(self, app, client):
        """Test registration with unauthorized email."""
        with app.app_context():
            app.config['ALLOWED_EMAILS'] = {'allowed@example.com'}
            
            response = client.post('/auth/register', data={
                'email': 'unauthorized@example.com',
                'password': 'SecurePass1',
                'confirm_password': 'SecurePass1'
            }, follow_redirects=True)
            
            assert b'autorizado' in response.data.lower()
    
    def test_register_duplicate_email(self, client, sample_user, app):
        """Test registration with existing email."""
        with app.app_context():
            app.config['ALLOWED_EMAILS'] = set()  # Allow all
            
            response = client.post('/auth/register', data={
                'email': 'test@example.com',  # Already exists
                'password': 'SecurePass1',
                'confirm_password': 'SecurePass1'
            }, follow_redirects=True)
            
            assert b'registrado' in response.data.lower()
    
    def test_register_password_mismatch(self, app, client):
        """Test registration with mismatched passwords."""
        with app.app_context():
            app.config['ALLOWED_EMAILS'] = set()
            
            response = client.post('/auth/register', data={
                'email': 'new@example.com',
                'password': 'SecurePass1',
                'confirm_password': 'DifferentPass1'
            }, follow_redirects=True)
            
            assert b'coincidir' in response.data.lower()


class TestProtectedRoutes:
    """Tests for route protection."""
    
    def test_index_requires_login(self, client):
        """Test that index redirects unauthenticated users."""
        response = client.get('/', follow_redirects=False)
        
        assert response.status_code == 302
        assert 'login' in response.location
    
    def test_patients_requires_login(self, client):
        """Test that patients page requires login."""
        response = client.get('/patients/', follow_redirects=False)
        
        assert response.status_code == 302
        assert 'login' in response.location
    
    def test_add_session_requires_login(self, client):
        """Test that add session page requires login."""
        response = client.get('/sessions/add', follow_redirects=False)
        
        assert response.status_code == 302
