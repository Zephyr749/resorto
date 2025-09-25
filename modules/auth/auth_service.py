import os
from fastapi import HTTPException
import jwt
from modules.auth.auth_repo import AuthRepository
from modules.common.logger import get_logger
from modules.db.schemas import UserCreate, User, LoginResponse
from datetime import datetime, timedelta, timezone


logger = get_logger(__name__)
repository = AuthRepository()
JWT_SECRET = os.getenv('JWT_SECRET')

def registerUser(user:UserCreate):
    existingUser = repository.getUserByEmail(user.email)
    if existingUser:
        raise HTTPException(status_code=400, detail="User already exists")
    response = repository.insertUser(user)
    userId = response.inserted_id

    return buildUserObject(user, userId)


def buildUserObject(userDetails, userId) -> User:
    jwtPayload = {
        'userId': str(userId),
        'expirationTime': str(datetime.now(timezone.utc) + timedelta(days=7))
    }
    jwtToken = jwt.encode(jwtPayload, JWT_SECRET)
    user:User = userDetails.model_copy(update={
        'id': userId,
        'fullName': userDetails.firstName + ' ' + userDetails.lastName,
    })
    user.password = None
    response: LoginResponse = LoginResponse(
        user=user,
        token=jwtToken
    )
    return response