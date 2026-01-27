from pydantic import BaseModel


class UploadRequest(BaseModel):
    filename: str
    content_type: str
    folder: str = "misc" # e.g. "blogs", "projects"

class PresignedUrlResponse(BaseModel):
    upload_url: str
    public_url: str
    key: str