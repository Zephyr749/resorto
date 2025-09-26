import os
from fastapi import HTTPException
import jwt
from modules.auth.auth_repo import AuthRepository
from modules.common.logger import get_logger
from modules.db.schemas import UserCreate, User, LoginResponse, Credentials
from datetime import datetime, timedelta, timezone
from modules.common.utils import PasswordHelper

logger = get_logger(__name__)
repository = AuthRepository()
JWT_SECRET = os.getenv('JWT_SECRET')

def registerUser(user:UserCreate):
    hashedPassword = PasswordHelper.hash_password(user.password)
    user.password = hashedPassword
    existingUser = repository.getUserByEmail(user.email)
    if existingUser:
        raise HTTPException(status_code=400, detail="User already exists")
    response = repository.insertUser(user)
    userId = str(response.inserted_id)
    return buildUserObject(user, userId)

def buildUserObject(userDetails, userId) -> User:
    jwtPayload = {
        'userId': str(userId),
        'expirationTime': str(datetime.now(timezone.utc) + timedelta(days=7))
    }

    jwtToken = jwt.encode(jwtPayload, JWT_SECRET)
    userDict = userDetails if isinstance(userDetails, dict) else userDetails.dict()
    user: User = User(
        id=userId,
        **userDict,
        fullName=userDict['firstName'] + ' ' + userDict['lastName'],
    )
    response: LoginResponse = LoginResponse(
        user=user,
        token=jwtToken
    )
    return response

def loginUser(credentials: Credentials) -> LoginResponse:
    user = repository.getUserByEmail(credentials.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not PasswordHelper.verify_password(credentials.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return buildUserObject(user, str(user['_id']))