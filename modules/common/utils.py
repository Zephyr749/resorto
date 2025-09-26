import bcrypt
import re


class PasswordHelper:
    def __init__(self, password):
        self.password = password

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @classmethod
    def verify_password(self, password: str, storedPassword: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), storedPassword.encode('utf-8'))


class Validator:
    @staticmethod
    def email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+%-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def password(password: str) -> {str, str}:
        result = {
            'isValid': False,
            'message': None,
        }
        if len(password) < 8:
            result['message'] = 'Password must be at least 8 characters long'
        elif not re.search(r'[A-Z]', password):
            result['message'] = 'Password does not contain at least one uppercase letter'
        elif not re.search(r'[a-z]', password):
            result['message'] = 'Password does not contain at least one lowercase letter'
        elif not re.search(r'[0-9]', password):
            result['message'] = 'Password does not contain at least one number'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            result['message'] = 'Password does not contain at least one special character'

        if not result['message']:
            result['isValid'] = True

        return result

    @classmethod
    def credentials(cls, creds: dict):
        if not cls.email(creds.email):
            raise ValueError('Invalid email')
        password_response = cls.password(creds.password)
        print(f'Password response: {password_response}')
        if not password_response['isValid']:
            raise ValueError(password_response.message)


def build_response(success: bool, data, message: str = '') -> dict:
    if success:
        return {
            'success': True,
            'data': data if data else None,
            'message': message,
        }
    else:
        return {
            'success': False,
            'error': data if data else None,
            'message': message,
        }