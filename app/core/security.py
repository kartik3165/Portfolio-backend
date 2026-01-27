import os
from fastapi import HTTPException, status
from dotenv import load_dotenv
load_dotenv()

def verify_passkey(passkey: str):
    admin_key = os.getenv("PASSKEY")
    if not admin_key or passkey != admin_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid passkey",
        )

from fastapi import Depends, HTTPException, status, Request
from app.services.token import TokenService

async def get_current_admin(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    scheme, _, token_str = token.partition(" ")
    if scheme.lower() != "bearer":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Invalid token scheme"
         )

    payload = TokenService.verify_token(token_str)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return payload