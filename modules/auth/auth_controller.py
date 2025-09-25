from contextvars import Token
from logging import getLogger
from fastapi import APIRouter

from modules.common.utils import Validator, PasswordHelper, build_response
from modules.db.schemas import UserCreate
from modules.auth.auth_service import registerUser
logger = getLogger(__name__)
router = APIRouter()

@router.post("/register")
def register(user:UserCreate):
    try:
        Validator.credentials(user)
        hashedPassword = PasswordHelper.hash_password(user.password)
        user.password = hashedPassword
        response = registerUser(user)
        logger.info(f'response: {response}')
        return build_response(True, response, 'User registered successfully')
    except ValueError as e:
        print(e)
        logger.error(f'error: {e}')
        return build_response(False, str(e), 'Invalid input')
    except Exception as e:
        logger.error(f'error: {e}')
        return build_response(False, str(e), 'Failed to register user')

@router.post("/login")
def login(credentials):
    pass