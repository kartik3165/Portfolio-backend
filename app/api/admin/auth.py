from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import verify_passkey

router = APIRouter(prefix="", tags=["Auth (Admin)"])

class PasskeyRequest(BaseModel):
    passkey: str

@router.post("/verify-passkey")
def check_passkey(payload: PasskeyRequest):
    """
    Verify if the provided passkey is correct.
    Returns {"valid": true} if correct, otherwise raises 401.
    """
    verify_passkey(payload.passkey)
    return {"valid": True}
