from pydantic import BaseModel

class User(BaseModel):
    email: str
    fullName: str
    firstName: str
    lastName: str

class UserCreate(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str

class LoginResponse(BaseModel):
    user: User
    token: str
