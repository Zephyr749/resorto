from fastapi import Header, HTTPException, status
import jwt
from modules.common.config import config
from modules.common.logger import get_logger

logger = get_logger(__name__)

def verify_token(authorization: str = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header missing'
        )
    
    try:
        if authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
        else:
            token = authorization
            
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired'
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )

def get_current_user_id(authorization: str = Header(None)) -> str:
    payload = verify_token(authorization)
    user_id = payload.get('userId')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token payload'
        )
    return user_id
