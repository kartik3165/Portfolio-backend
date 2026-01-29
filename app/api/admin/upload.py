from fastapi import APIRouter, HTTPException, Depends,UploadFile, File, Form
from app.services.storage import StorageService
from app.schemas.upload import UploadRequest, PresignedUrlResponse
from app.core.security import verify_passkey
from uuid6 import uuid7
from typing import Dict

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/presigned-url", response_model=PresignedUrlResponse)
def generate_presigned_url(request: UploadRequest):
    verify_passkey(request.passkey)
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


@router.post("/upload-file", response_model=Dict[str, str])
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Form(...),
    passkey: str = Form(...)
):
    """
    Upload file directly through backend to R2.
    This avoids CORS issues with presigned URLs.
    """
    verify_passkey(passkey)
    try:
        service = StorageService()
        
        # Read file content
        content = await file.read()
        
        # Generate unique filename
        ext = file.filename.split('.')[-1] if '.' in file.filename else "" # type: ignore
        unique_name = f"{uuid7()}.{ext}" if ext else f"{uuid7()}"
        key = f"{folder}/{unique_name}"
        
        # Upload directly to R2
        service.s3_client.put_object(
            Bucket=service.bucket_name,
            Key=key,
            Body=content,
            ContentType=file.content_type or 'application/octet-stream'
        )
        
        base_url = (service.public_base_url or "").rstrip("/")
        public_url = f"{base_url}/{key}"
        
        return {
            "public_url": public_url,
            "key": key
        }
        
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")