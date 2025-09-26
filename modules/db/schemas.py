from pydantic import BaseModel

class User(BaseModel):
    id: str
    email: str
    fullName: str
    firstName: str
    lastName: str

class UserCreate(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str

class DBUser(BaseModel):
    _id: str
    email: str
    password: str
    firstName: str
    lastName: str

class LoginResponse(BaseModel):
    user: User
    token: str

class Credentials(BaseModel):
    email: str
    password: str
