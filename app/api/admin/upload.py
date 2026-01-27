from fastapi import APIRouter, HTTPException, Depends
from app.services.storage import StorageService
from botocore.exceptions import ClientError
from app.schemas.upload import UploadRequest, PresignedUrlResponse
from uuid6 import uuid7
from app.core.security import get_current_admin

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/presigned-url", response_model=PresignedUrlResponse)
def generate_presigned_url(request: UploadRequest, admin: dict = Depends(get_current_admin)):
    try:
        service = StorageService()
        ext = request.filename.split('.')[-1] if '.' in request.filename else ""
        unique_name = f"{uuid7()}.{ext}" if ext else f"{uuid7()}"
        key = f"{request.folder}/{unique_name}"
        
        return service.generate_presigned_url(key, request.content_type)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate upload URL")
