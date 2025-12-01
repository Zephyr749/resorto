from fastapi import HTTPException
import jwt
from modules.auth.auth_repo import AuthRepository
from modules.common.logger import get_logger
from modules.db.schemas import UserCreate, User, LoginResponse, Credentials
from datetime import datetime, timedelta, timezone
from modules.common.utils import PasswordHelper
from modules.common.config import config

logger = get_logger(__name__)
repository = AuthRepository()


def registerUser(user: UserCreate):
    hashedPassword = PasswordHelper.hash_password(user.password)
    user.password = hashedPassword
    existingUser = repository.getUserByEmail(user.email)
    if existingUser:
        raise HTTPException(status_code=400, detail='User already exists')
    response = repository.insertUser(user)
    userId = str(response.inserted_id)
    return buildUserObject(user, userId)


def buildUserObject(userDetails, userId) -> User:
    jwtPayload = {
        'userId': str(userId),
        'expirationTime': str(datetime.now(timezone.utc) + timedelta(days=config.JWT_EXPIRATION_DAYS)),
    }

    jwtToken = jwt.encode(jwtPayload, config.JWT_SECRET, algorithm='HS256')
    userDict = userDetails if isinstance(userDetails, dict) else userDetails.model_dump()
    user: User = User(
        id=userId,
        **userDict,
        fullName=userDict['firstName'] + ' ' + userDict['lastName'],
    )
    response: LoginResponse = LoginResponse(user=user, token=jwtToken)
    return response


def loginUser(credentials: Credentials) -> LoginResponse:
    user = repository.getUserByEmail(credentials.email)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not PasswordHelper.verify_password(credentials.password, user['password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return buildUserObject(user, str(user['_id']))


def getUserProfile(userId: str) -> User:
    user = repository.getUserById(userId)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    return User(
        id=str(user['_id']),
        email=user['email'],
        firstName=user['firstName'],
        lastName=user['lastName'],
        fullName=user['firstName'] + ' ' + user['lastName'],
        role=user.get('role', 'user')
    )


def updateUserProfile(userId: str, firstName: str, lastName: str) -> User:
    user = repository.getUserById(userId)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    repository.updateUser(userId, firstName, lastName)
    
    return User(
        id=userId,
        email=user['email'],
        firstName=firstName,
        lastName=lastName,
        fullName=firstName + ' ' + lastName,
        role=user.get('role', 'user')
    )


def changePassword(userId: str, currentPassword: str, newPassword: str) -> dict:
    user = repository.getUserById(userId)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    if not PasswordHelper.verify_password(currentPassword, user['password']):
        raise HTTPException(status_code=401, detail='Current password is incorrect')
    
    hashedPassword = PasswordHelper.hash_password(newPassword)
    repository.updatePassword(userId, hashedPassword)
    
    return {'message': 'Password changed successfully'}
