from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(BaseModel):
    id: str
    email: str
    fullName: str
    firstName: str
    lastName: str
    role: UserRole = UserRole.USER

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    role: UserRole = UserRole.USER

class UserUpdate(BaseModel):
    firstName: str
    lastName: str

class PasswordChange(BaseModel):
    currentPassword: str
    newPassword: str

class DBUser(BaseModel):
    _id: str
    email: str
    password: str
    firstName: str
    lastName: str
    role: UserRole = UserRole.USER

class LoginResponse(BaseModel):
    user: User
    token: str

class Credentials(BaseModel):
    email: EmailStr
    password: str
