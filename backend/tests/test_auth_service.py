import pytest
import uuid
from fastapi import HTTPException
from modules.auth.auth_service import registerUser, loginUser, getUserProfile, updateUserProfile, changePassword
from modules.auth.auth_repo import AuthRepository
from modules.db.schemas import UserCreate, Credentials
from modules.common.utils import PasswordHelper

class TestAuthService:
    @pytest.fixture
    def repo(self):
        return AuthRepository()

    def test_register_user_success(self, repo):
        sample_user = {
            'email': f'register_success-{uuid.uuid4()}@example.com',
            'password': 'TestPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user_create = UserCreate(**sample_user)
        response = registerUser(user_create)
        
        assert response.user.email == sample_user['email']
        assert response.user.firstName == sample_user['firstName']
        assert response.user.fullName == f"{sample_user['firstName']} {sample_user['lastName']}"
        assert response.token is not None
        assert len(response.token) > 0

    def test_register_user_duplicate_email(self, repo):
        sample_user = {
            'email': f'duplicate2-{uuid.uuid4()}@example.com',
            'password': 'TestPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user_create = UserCreate(**sample_user)
        registerUser(user_create)
        
        user_create2 = UserCreate(**sample_user)
        with pytest.raises(HTTPException) as exc_info:
            registerUser(user_create2)
        
        assert exc_info.value.status_code == 400
        assert 'already exists' in str(exc_info.value.detail)

    def test_login_user_success(self, repo):
        sample_user = {
            'email': f'login_success-{uuid.uuid4()}@example.com',
            'password': 'TestPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user_create = UserCreate(**sample_user)
        registerUser(user_create)
        
        credentials = Credentials(email=sample_user['email'], password=sample_user['password'])
        response = loginUser(credentials)
        
        assert response.user.email == sample_user['email']
        assert response.token is not None

    def test_login_user_not_found(self, repo):
        credentials = Credentials(email='nonexistent@example.com', password='Password123!')
        
        with pytest.raises(HTTPException) as exc_info:
            loginUser(credentials)
        
        assert exc_info.value.status_code == 404
        assert 'not found' in str(exc_info.value.detail)

    def test_login_user_wrong_password(self, repo):
        sample_user = {
            'email': f'login_wrong-{uuid.uuid4()}@example.com',
            'password': 'TestPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user_create = UserCreate(**sample_user)
        registerUser(user_create)
        
        credentials = Credentials(email=sample_user['email'], password='WrongPassword123!')
        
        with pytest.raises(HTTPException) as exc_info:
            loginUser(credentials)
        
        assert exc_info.value.status_code == 401
        assert 'Invalid credentials' in str(exc_info.value.detail)

    def test_get_user_profile_success(self, repo):
        sample_user = {
            'email': f'profile_get-{uuid.uuid4()}@example.com',
            'password': 'TestPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user_create = UserCreate(**sample_user)
        response = registerUser(user_create)
        user_id = response.user.id
        
        profile = getUserProfile(user_id)
        
        assert profile.id == user_id
        assert profile.email == sample_user['email']
        assert profile.firstName == sample_user['firstName']

    def test_get_user_profile_not_found(self, repo):
        from bson import ObjectId
        fake_id = str(ObjectId())
        
        with pytest.raises(HTTPException) as exc_info:
            getUserProfile(fake_id)
        
        assert exc_info.value.status_code == 404

    def test_update_user_profile_success(self, repo):
        sample_user = {
            'email': f'profile_update-{uuid.uuid4()}@example.com',
            'password': 'TestPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user_create = UserCreate(**sample_user)
        response = registerUser(user_create)
        user_id = response.user.id
        
        updated = updateUserProfile(user_id, 'Jane', 'Smith')
        
        assert updated.firstName == 'Jane'
        assert updated.lastName == 'Smith'
        assert updated.fullName == 'Jane Smith'

    def test_update_user_profile_not_found(self, repo):
        from bson import ObjectId
        fake_id = str(ObjectId())
        
        with pytest.raises(HTTPException) as exc_info:
            updateUserProfile(fake_id, 'Jane', 'Smith')
        
        assert exc_info.value.status_code == 404

    def test_change_password_success(self, repo):
        sample_user = {
            'email': f'change_pass2-{uuid.uuid4()}@example.com',
            'password': 'TestPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user_create = UserCreate(**sample_user)
        response = registerUser(user_create)
        user_id = response.user.id
        
        result = changePassword(user_id, sample_user['password'], 'NewPassword123!')
        
        assert result['message'] == 'Password changed successfully'
        
        # Verify the password was updated by trying to login with new password
        credentials = Credentials(email=sample_user['email'], password='NewPassword123!')
        login_response = loginUser(credentials)
        assert login_response.user.email == sample_user['email']

    def test_change_password_wrong_current(self, repo):
        sample_user = {
            'email': f'change_pass_wrong-{uuid.uuid4()}@example.com',
            'password': 'TestPass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user_create = UserCreate(**sample_user)
        response = registerUser(user_create)
        user_id = response.user.id
        
        with pytest.raises(HTTPException) as exc_info:
            changePassword(user_id, 'WrongPassword123!', 'NewPassword123!')
        
        assert exc_info.value.status_code == 401
        assert 'incorrect' in str(exc_info.value.detail)

    def test_change_password_user_not_found(self, repo):
        from bson import ObjectId
        fake_id = str(ObjectId())
        
        with pytest.raises(HTTPException) as exc_info:
            changePassword(fake_id, 'OldPass123!', 'NewPass123!')
        
        assert exc_info.value.status_code == 404
