import pytest
from modules.auth.auth_repo import AuthRepository
from modules.db.schemas import UserCreate
from bson import ObjectId

class TestAuthRepository:
    @pytest.fixture
    def repo(self):
        return AuthRepository()

    def test_insert_user(self, repo, sample_user):
        user_create = UserCreate(**sample_user)
        result = repo.insertUser(user_create)
        
        assert result.inserted_id is not None
        
        inserted_user = repo.getUserByEmail(sample_user['email'])
        assert inserted_user is not None
        assert inserted_user['email'] == sample_user['email']

    def test_get_user_by_email_exists(self, repo, sample_user):
        user_create = UserCreate(**sample_user)
        repo.insertUser(user_create)
        
        user = repo.getUserByEmail(sample_user['email'])
        
        assert user is not None
        assert user['email'] == sample_user['email']
        assert user['firstName'] == sample_user['firstName']

    def test_get_user_by_email_not_exists(self, repo):
        user = repo.getUserByEmail('nonexistent@example.com')
        assert user is None

    def test_get_user_by_id_exists(self, repo, sample_user):
        user_create = UserCreate(**sample_user)
        result = repo.insertUser(user_create)
        user_id = str(result.inserted_id)
        
        user = repo.getUserById(user_id)
        
        assert user is not None
        assert user['email'] == sample_user['email']

    def test_get_user_by_id_not_exists(self, repo):
        fake_id = str(ObjectId())
        user = repo.getUserById(fake_id)
        assert user is None

    def test_update_user(self, repo, sample_user):
        user_create = UserCreate(**sample_user)
        result = repo.insertUser(user_create)
        user_id = str(result.inserted_id)
        
        repo.updateUser(user_id, 'Jane', 'Smith')
        
        updated_user = repo.getUserById(user_id)
        assert updated_user['firstName'] == 'Jane'
        assert updated_user['lastName'] == 'Smith'

    def test_update_password(self, repo, sample_user):
        user_create = UserCreate(**sample_user)
        result = repo.insertUser(user_create)
        user_id = str(result.inserted_id)
        
        new_password = 'NewHashedPassword123!'
        repo.updatePassword(user_id, new_password)
        
        updated_user = repo.getUserById(user_id)
        assert updated_user['password'] == new_password
