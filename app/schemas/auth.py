from pydantic import BaseModel, EmailStr
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

# Admin Credential Management
class AdminAuthResponse(BaseModel):
    """Response model for GET/PUT /admin/auth - returns email and success status"""
    email: str
    valid: bool = True


class AdminAuthInit(BaseModel):
    """Response model for POST /admin/auth/init"""
    message: str
    email: str


class AdminAuthUpdate(BaseModel):
    """Request model for PUT /admin/auth"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    passkey: str  


class AdminLoginRequest(BaseModel):
    """Request model for admin login"""
    email: EmailStr
    password: str
