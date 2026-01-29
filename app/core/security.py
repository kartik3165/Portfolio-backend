import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

def verify_passkey(passkey: str):
    admin_key = os.getenv("PASSKEY")
    if not admin_key:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Passkey not configured",
        )
    if passkey != admin_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid passkey",
        )
