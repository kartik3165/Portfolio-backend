from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    username: str
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    password: str
    passkey: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPD(BaseModel):
    username: str | None = None
