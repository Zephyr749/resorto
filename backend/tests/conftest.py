import pytest
import mongomock
from modules.db.mongo_client import MongoDBClient

@pytest.fixture(scope="function", autouse=True)
def mock_mongo(monkeypatch):
    mock_client = mongomock.MongoClient()
    mock_db = mock_client['test_db']
    
    def mock_get_instance():
        instance = MongoDBClient.__new__(MongoDBClient)
        instance.client = mock_client
        instance.db = mock_db
        return instance
    
    monkeypatch.setattr(MongoDBClient, 'get_instance', mock_get_instance)
    MongoDBClient._instance = None
    
    yield mock_db
    
    # Clean up after each test
    for collection in list(mock_db.list_collection_names()):
        mock_db.drop_collection(collection)
    
    MongoDBClient._instance = None

@pytest.fixture
def sample_user():
    return {
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'firstName': 'John',
        'lastName': 'Doe'
    }

@pytest.fixture
def sample_user_hashed(sample_user):
    from modules.common.utils import PasswordHelper
    user = sample_user.copy()
    user['password'] = PasswordHelper.hash_password(user['password'])
    return user
