from fastapi import Header, HTTPException, status, Depends
from modules.common.auth_middleware import verify_token
from modules.auth.auth_repo import AuthRepository
from modules.common.logger import get_logger

logger = get_logger(__name__)
repository = AuthRepository()

def require_admin(authorization: str = Header(None)) -> str:
    """
    Middleware to verify that the user is an admin.
    Returns the user ID if the user is an admin, raises HTTPException otherwise.
    """
    payload = verify_token(authorization)
    user_id = payload.get('userId')
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token payload'
        )
    
    # Get user from database to check role
    user = repository.getUserById(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    user_role = user.get('role', 'user')
    if user_role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin access required'
        )
    
    return user_id
