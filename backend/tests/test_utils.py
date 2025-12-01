import pytest
from modules.common.utils import PasswordHelper, Validator, build_response

class TestPasswordHelper:
    def test_hash_password(self):
        password = 'TestPassword123!'
        hashed = PasswordHelper.hash_password(password)
        
        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        password = 'TestPassword123!'
        hashed = PasswordHelper.hash_password(password)
        
        assert PasswordHelper.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        password = 'TestPassword123!'
        hashed = PasswordHelper.hash_password(password)
        
        assert PasswordHelper.verify_password('WrongPassword123!', hashed) is False

class TestValidator:
    def test_email_valid(self):
        assert Validator.email('test@example.com') is True
        assert Validator.email('user.name+tag@example.co.uk') is True

    def test_email_invalid(self):
        assert Validator.email('invalid') is False
        assert Validator.email('invalid@') is False
        assert Validator.email('@example.com') is False
        assert Validator.email('invalid@.com') is False

    def test_password_valid(self):
        result = Validator.password('ValidPass123!')
        assert result['isValid'] is True
        assert result['message'] is None

    def test_password_too_short(self):
        result = Validator.password('Short1!')
        assert result['isValid'] is False
        assert 'at least 8 characters' in result['message']

    def test_password_no_uppercase(self):
        result = Validator.password('lowercase123!')
        assert result['isValid'] is False
        assert 'uppercase' in result['message']

    def test_password_no_lowercase(self):
        result = Validator.password('UPPERCASE123!')
        assert result['isValid'] is False
        assert 'lowercase' in result['message']

    def test_password_no_number(self):
        result = Validator.password('NoNumbers!')
        assert result['isValid'] is False
        assert 'number' in result['message']

    def test_password_no_special(self):
        result = Validator.password('NoSpecial123')
        assert result['isValid'] is False
        assert 'special character' in result['message']

    def test_credentials_valid(self):
        from modules.db.schemas import UserCreate
        user = UserCreate(
            email='test@example.com',
            password='ValidPass123!',
            firstName='John',
            lastName='Doe'
        )
        Validator.credentials(user)

    def test_credentials_invalid_email(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            from modules.db.schemas import UserCreate
            user = UserCreate(
                email='invalid-email',
                password='ValidPass123!',
                firstName='John',
                lastName='Doe'
            )

    def test_credentials_invalid_password(self):
        from modules.db.schemas import UserCreate
        user = UserCreate(
            email='test@example.com',
            password='weak',
            firstName='John',
            lastName='Doe'
        )
        with pytest.raises(ValueError):
            Validator.credentials(user)

class TestBuildResponse:
    def test_build_response_success(self):
        response = build_response(True, {'id': '123'}, 'Success message')
        
        assert response['success'] is True
        assert response['data'] == {'id': '123'}
        assert response['message'] == 'Success message'

    def test_build_response_failure(self):
        response = build_response(False, 'Error details', 'Error message')
        
        assert response['success'] is False
        assert response['error'] == 'Error details'
        assert response['message'] == 'Error message'

    def test_build_response_no_data(self):
        response = build_response(True, None, 'Success')
        
        assert response['success'] is True
        assert response['data'] is None
        assert response['message'] == 'Success'
