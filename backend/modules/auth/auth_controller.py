from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, status, Response

from modules.common.utils import Validator, build_response
from modules.db.schemas import UserCreate, Credentials, UserUpdate, PasswordChange
from modules.auth.auth_service import registerUser, loginUser, getUserProfile, updateUserProfile, changePassword
from modules.common.auth_middleware import get_current_user_id

logger = getLogger(__name__)
router = APIRouter()

@router.post('/register')
def register(user: UserCreate, response: Response):
    try:
        Validator.credentials(user)
        result = registerUser(user)
        logger.info(f'User registered: {user.email}')
        return build_response(True, result, 'User registered successfully')
    except ValueError as e:
        logger.error(f'Validation error: {e}')
        response.status_code = status.HTTP_400_BAD_REQUEST
        return build_response(False, str(e), 'Invalid input')
    except HTTPException as he:
        # HTTPException from service layer - use its status code
        logger.error(f'Error: {he.detail}')
        response.status_code = he.status_code
        return build_response(False, str(he.detail), 'Registration failed')
    except Exception as e:
        logger.error(f'Unexpected error during registration: {e}')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to register user')

@router.post('/login')
def login(credentials: Credentials, response: Response):
    try:
        result = loginUser(credentials)
        logger.info(f'User logged in: {credentials.email}')
        return build_response(True, result, 'Login successful')
    except HTTPException as he:
        # HTTPException from service layer (401, 404, etc.)
        logger.error(f'Login failed for {credentials.email}: {he.detail}')
        response.status_code = he.status_code
        return build_response(False, str(he.detail), 'Login failed')
    except ValueError as e:
        logger.error(f'Validation error: {e}')
        response.status_code = status.HTTP_400_BAD_REQUEST
        return build_response(False, str(e), 'Invalid input')
    except Exception as e:
        logger.error(f'Unexpected error during login: {e}')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Login failed')

@router.get('/profile')
def get_profile(response: Response, user_id: str = Depends(get_current_user_id)):
    try:
        profile = getUserProfile(user_id)
        return build_response(True, profile, 'Profile retrieved successfully')
    except HTTPException as he:
        logger.error(f'Error retrieving profile: {he.detail}')
        response.status_code = he.status_code
        return build_response(False, str(he.detail), 'Failed to retrieve profile')
    except Exception as e:
        logger.error(f'Unexpected error retrieving profile: {e}')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to retrieve profile')

@router.put('/profile')
def update_profile(userUpdate: UserUpdate, response: Response, user_id: str = Depends(get_current_user_id)):
    try:
        updated_user = updateUserProfile(user_id, userUpdate.firstName, userUpdate.lastName)
        logger.info(f'Profile updated for user: {user_id}')
        return build_response(True, updated_user, 'Profile updated successfully')
    except HTTPException as he:
        logger.error(f'Error updating profile: {he.detail}')
        response.status_code = he.status_code
        return build_response(False, str(he.detail), 'Failed to update profile')
    except Exception as e:
        logger.error(f'Unexpected error updating profile: {e}')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to update profile')

@router.post('/change-password')
def change_user_password(passwordChange: PasswordChange, response: Response, user_id: str = Depends(get_current_user_id)):
    try:
        password_result = Validator.password(passwordChange.newPassword)
        if not password_result['isValid']:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return build_response(False, password_result['message'], 'Invalid password')
        result = changePassword(user_id, passwordChange.currentPassword, passwordChange.newPassword)
        logger.info(f'Password changed for user: {user_id}')
        return build_response(True, result, 'Password changed successfully')
    except HTTPException as he:
        logger.error(f'Error changing password: {he.detail}')
        response.status_code = he.status_code
        return build_response(False, str(he.detail), 'Failed to change password')
    except ValueError as e:
        logger.error(f'Validation error: {e}')
        response.status_code = status.HTTP_400_BAD_REQUEST
        return build_response(False, str(e), 'Invalid input')
    except Exception as e:
        logger.error(f'Unexpected error changing password: {e}')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return build_response(False, str(e), 'Failed to change password')
    