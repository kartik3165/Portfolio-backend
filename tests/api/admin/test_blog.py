from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_blog_success():
    payload = {
        "passkey": "secret",
        "slug": "test-blog",
        "title": "Test Blog",
        "excerpt": "Blog excerpt",
        "author": "Author Name",
        "date": "2023-01-01",
        "readtime": "5 min",
        "image": "http://image.com/blog.png",
        "gallery": [],
        "tags": ["Tag1"],
        "content": "Blog content"
    }

    mock_response = {
        "id": "123",
        **{k: v for k, v in payload.items() if k != "passkey"},
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    with patch("app.api.admin.blog.verify_passkey") as mock_verify:
        with patch("app.api.admin.blog.BlogRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            # Since create_blog is async, we use AsyncMock
            mock_instance.create_blog = AsyncMock(return_value=mock_response)

            response = client.post("/admin/blog", json=payload)
            
            assert response.status_code == 200
            assert response.json() == mock_response
            mock_instance.create_blog.assert_called_once()
            mock_verify.assert_called_once_with("secret")

def test_update_blog_success():
    blog_id = "123"
    payload = {
        "passkey": "secret",
        "title": "Updated Blog Title"
    }

    expected_response = {
        "id": blog_id,
        "title": "Updated Blog Title",
        "slug": "test-blog",
        "excerpt": "Blog excerpt",
        "author": "Author Name",
        "date": "2023-01-01",
        "readtime": "5 min",
        "image": "http://image.com/blog.png",
        "gallery": [],
        "tags": ["Tag1"],
        "content": "Blog content",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    with patch("app.api.admin.blog.verify_passkey") as mock_verify:
        with patch("app.api.admin.blog.BlogRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.update_blog = AsyncMock(return_value=expected_response)

            response = client.put(f"/admin/blog/{blog_id}", json=payload)
            
            assert response.status_code == 200
            assert response.json() == expected_response
            mock_instance.update_blog.assert_called_once()
            mock_verify.assert_called_once_with("secret")

def test_update_blog_not_found():
    blog_id = "nonexistent"
    payload = {
        "passkey": "secret",
        "title": "Updated Blog Title"
    }

    with patch("app.api.admin.blog.verify_passkey") as mock_verify:
        with patch("app.api.admin.blog.BlogRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.update_blog = AsyncMock(return_value=None)

            response = client.put(f"/admin/blog/{blog_id}", json=payload)
            
            assert response.status_code == 404

def test_delete_blog_success():
    blog_id = "123"
    payload = {"passkey": "secret"}

    with patch("app.api.admin.blog.verify_passkey") as mock_verify:
        with patch("app.api.admin.blog.BlogRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.delete_blog = AsyncMock(return_value=True)

            response = client.request("DELETE", f"/admin/blog/{blog_id}", json=payload)
            
            assert response.status_code == 200
            assert response.json() == {"message": f"Blog deleted successfully of id {blog_id}"}
            mock_instance.delete_blog.assert_called_once_with(blog_id)
            mock_verify.assert_called_once_with("secret")
