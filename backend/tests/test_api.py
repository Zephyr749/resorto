import pytest
import uuid
from fastapi.testclient import TestClient
from main import app
from modules.auth.auth_repo import AuthRepository
from modules.db.schemas import UserCreate
from modules.common.utils import PasswordHelper

client = TestClient(app)

class TestAuthAPI:
    def test_register_success(self):
        unique_email = f'newuser-{uuid.uuid4()}@example.com'
        response = client.post('/auth/register', json={
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'token' in data['data']
        assert data['data']['user']['email'] == unique_email

    def test_register_invalid_email(self):
        response = client.post('/auth/register', json={
            'email': 'invalid-email',
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        })
        
        assert response.status_code == 422

    def test_register_weak_password(self):
        unique_email = f'test-{uuid.uuid4()}@example.com'
        response = client.post('/auth/register', json={
            'email': unique_email,
            'password': 'weak',
            'firstName': 'John',
            'lastName': 'Doe'
        })
        
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert 'error' in data

    def test_register_duplicate_email(self):
        unique_email = f'duplicate-{uuid.uuid4()}@example.com'
        user_data = {
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        
        client.post('/auth/register', json=user_data)
        response = client.post('/auth/register', json=user_data)
        
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert 'already exists' in data['error']

    def test_login_success(self):
        unique_email = f'logintest-{uuid.uuid4()}@example.com'
        user_data = {
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        client.post('/auth/register', json=user_data)
        
        response = client.post('/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'token' in data['data']

    def test_login_wrong_password(self):
        unique_email = f'wrongpass-{uuid.uuid4()}@example.com'
        user_data = {
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        client.post('/auth/register', json=user_data)
        
        response = client.post('/auth/login', json={
            'email': user_data['email'],
            'password': 'WrongPassword123!'
        })
        
        assert response.status_code == 401
        data = response.json()
        assert data['success'] is False
        assert 'error' in data

    def test_login_user_not_found(self):
        response = client.post('/auth/login', json={
            'email': 'notfound@example.com',
            'password': 'Password123!'
        })
        
        assert response.status_code == 404
        data = response.json()
        assert data['success'] is False
        assert 'error' in data

    def test_get_profile_success(self):
        unique_email = f'profiletest-{uuid.uuid4()}@example.com'
        user_data = {
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        register_response = client.post('/auth/register', json=user_data)
        token = register_response.json()['data']['token']
        
        response = client.get('/auth/profile', headers={
            'Authorization': f'Bearer {token}'
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['email'] == user_data['email']

    def test_get_profile_no_token(self):
        response = client.get('/auth/profile')
        
        assert response.status_code == 401

    def test_get_profile_invalid_token(self):
        response = client.get('/auth/profile', headers={
            'Authorization': 'Bearer invalid_token'
        })
        
        assert response.status_code == 401

    def test_update_profile_success(self):
        unique_email = f'updatetest-{uuid.uuid4()}@example.com'
        user_data = {
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        register_response = client.post('/auth/register', json=user_data)
        token = register_response.json()['data']['token']
        
        response = client.put('/auth/profile', 
            json={
                'firstName': 'Jane',
                'lastName': 'Smith'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['firstName'] == 'Jane'
        assert data['data']['lastName'] == 'Smith'

    def test_update_profile_no_token(self):
        response = client.put('/auth/profile', json={
            'firstName': 'Jane',
            'lastName': 'Smith'
        })
        
        assert response.status_code == 401

    def test_change_password_success(self):
        unique_email = f'changepass-{uuid.uuid4()}@example.com'
        user_data = {
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        register_response = client.post('/auth/register', json=user_data)
        token = register_response.json()['data']['token']
        
        response = client.post('/auth/change-password',
            json={
                'currentPassword': 'ValidPass123!',
                'newPassword': 'NewValidPass123!'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    def test_change_password_wrong_current(self):
        unique_email = f'wrongcurrent-{uuid.uuid4()}@example.com'
        user_data = {
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        register_response = client.post('/auth/register', json=user_data)
        token = register_response.json()['data']['token']
        
        response = client.post('/auth/change-password',
            json={
                'currentPassword': 'WrongPassword123!',
                'newPassword': 'NewValidPass123!'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert data['success'] is False
        assert 'error' in data

    def test_change_password_weak_new(self):
        unique_email = f'weaknew-{uuid.uuid4()}@example.com'
        user_data = {
            'email': unique_email,
            'password': 'ValidPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        register_response = client.post('/auth/register', json=user_data)
        token = register_response.json()['data']['token']
        
        response = client.post('/auth/change-password',
            json={
                'currentPassword': 'ValidPass123!',
                'newPassword': 'weak'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert 'error' in data
