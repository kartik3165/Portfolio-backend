import os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from app.core.security import verify_passkey
from app.schemas.auth import AdminAuthResponse, AdminAuthInit, AdminAuthUpdate, AdminLoginRequest
from app.repositories.auth_repo import AuthRepo

router = APIRouter(prefix="", tags=["Auth (Admin)"])

class PasskeyRequest(BaseModel):
    passkey: str

@router.post("/verify-passkey")
async def check_passkey(payload: PasskeyRequest):
    """
    Verify if the provided passkey is correct.
    Returns {"valid": true} if correct, otherwise raises 401.
    """
    verify_passkey(payload.passkey)
    return {"valid": True}


# Admin Credential Management
@router.get("/auth", response_model=AdminAuthResponse)
async def get_admin_credentials(passkey: str = Header(..., alias="x-admin-passkey")):
    """Get current admin email (requires passkey)"""
    verify_passkey(passkey)
    repo = AuthRepo()
    
    creds = await repo.get_credentials()
    if not creds:
        raise HTTPException(status_code=404, detail="Admin credentials not initialized")
    
    return {"email": creds["email"], "valid": True}


@router.post("/auth/init", response_model=AdminAuthInit)
async def init_admin_credentials():
    """Initialize admin credentials from environment variables (one-time setup)"""
    repo = AuthRepo()
    
    # Check if already initialized
    if await repo.credentials_exist():
        raise HTTPException(status_code=409, detail="Admin credentials already initialized")
    
    # Get from environment variables
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    
    if not email or not password:
        raise HTTPException(
            status_code=500, 
            detail="ADMIN_EMAIL and ADMIN_PASSWORD environment variables must be set"
        )
    
    try:
        result = await repo.init_credentials(email, password)
        return {
            "message": "Admin credentials initialized successfully",
            "email": result["email"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize credentials: {str(e)}")


@router.put("/auth", response_model=AdminAuthResponse)
async def update_admin_credentials(payload: AdminAuthUpdate):
    """Update admin email and/or password (requires passkey)"""
    verify_passkey(payload.passkey)
    repo = AuthRepo()
    
    # Check if credentials exist
    if not await repo.credentials_exist():
        raise HTTPException(status_code=404, detail="Admin credentials not initialized")
    
    # At least one field must be provided
    if not payload.email and not payload.password:
        raise HTTPException(status_code=400, detail="At least one of email or password must be provided")
    
    try:
        updated = await repo.update_credentials(
            email=payload.email,
            password=payload.password
        )
        return {"email": updated["email"], "valid": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update credentials: {str(e)}")


@router.post("/login", response_model=AdminAuthResponse)
async def admin_login(payload: AdminLoginRequest):
    """Login with admin email and password"""
    repo = AuthRepo()
    
    # Ensure initialized
    creds = await repo.get_credentials()
    if not creds:
        raise HTTPException(status_code=404, detail="Admin credentials not initialized")
    
    # Verify email (normalized)
    if payload.email.lower().strip() != creds["email"]:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not await repo.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {"email": creds["email"], "valid": True}
