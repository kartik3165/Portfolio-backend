from pydantic import BaseModel


class UploadRequest(BaseModel):
    passkey: str
    filename: str
    content_type: str
    folder: str = "misc" # e.g. "blogs", "projects"

class PresignedUrlResponse(BaseModel):
    upload_url: str
    public_url: str
    key: str