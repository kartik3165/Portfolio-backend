from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_presigned_url_success():
    payload = {
        "filename": "test.png",
        "content_type": "image/png",
        "folder": "blogs"
    }

    mock_response = {
        "upload_url": "http://s3.upload/url",
        "public_url": "http://public.url/blogs/uuid.png",
        "key": "blogs/uuid.png"
    }

    with patch("app.api.admin.upload.StorageService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.generate_presigned_url.return_value = mock_response

        response = client.post("/admin/upload/presigned-url", json=payload)
        
        assert response.status_code == 200
        assert response.json() == mock_response
        mock_instance.generate_presigned_url.assert_called_once()
        # You could also check that it was called with correct arguments if you knew the uuid

def test_generate_presigned_url_failure():
    payload = {
        "filename": "test.png",
        "content_type": "image/png",
        "folder": "blogs"
    }

    with patch("app.api.admin.upload.StorageService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.generate_presigned_url.side_effect = Exception("S3 error")

        response = client.post("/admin/upload/presigned-url", json=payload)
        
        assert response.status_code == 500
        assert response.json()["detail"] == "Failed to generate upload URL"
