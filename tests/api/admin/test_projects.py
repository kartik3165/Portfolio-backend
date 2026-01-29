from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_project_success():
    payload = {
        "passkey": "secret",
        "slug": "test-project",
        "name": "Test Project",
        "subtitle": "A test project",
        "shortDesc": "Short description",
        "fullDesc": "Full description",
        "stats": [{"label": "Uptime", "value": "99%"}],
        "problem": "Problem statement",
        "solution": "Solution statement",
        "outcome": "Outcome statement",
        "architecture": ["Arch component"],
        "architectureImage": "http://image.com/arch.png",
        "challenges": ["Challenge 1"],
        "learnings": ["Learning 1"],
        "future": ["Future plan"],
        "tech": [{"name": "Python", "purpose": "backend"}],
        "coverImage": "http://image.com/cover.png",
        "color": "blue",
        "github": "http://github.com",
        "live": "http://live.com",
        "document": "http://doc.com",
        "features": ["Feature 1"],
        "screenshots": ["http://image.com/screen1.png"]
    }

    mock_response = {
        "id": "123",
        **{k: v for k, v in payload.items() if k != "passkey"},
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    with patch("app.api.admin.projects.verify_passkey") as mock_verify:
        with patch("app.api.admin.projects.ProjectRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.create_project.return_value = mock_response

            response = client.post("/admin/projects", json=payload)
            
            assert response.status_code == 200
            assert response.json() == mock_response
            mock_instance.create_project.assert_called_once()
            mock_verify.assert_called_once_with("secret")

def test_update_project_success():
    project_id = "123"
    payload = {
        "passkey": "secret",
        "name": "Updated Project"
    }
    
    expected_response = {
        "id": project_id,
        "name": "Updated Project",
        "slug": "test-project",
        "subtitle": "A test project",
        "shortDesc": "Short description",
        "fullDesc": "Full description",
        "stats": [{"label": "Uptime", "value": "99%"}],
        "problem": "Problem statement",
        "solution": "Solution statement",
        "outcome": "Outcome statement",
        "architecture": ["Arch component"],
        "architectureImage": "http://image.com/arch.png",
        "challenges": ["Challenge 1"],
        "learnings": ["Learning 1"],
        "future": ["Future plan"],
        "tech": [{"name": "Python", "purpose": "backend"}],
        "coverImage": "http://image.com/cover.png",
        "color": "blue",
        "github": "http://github.com",
        "live": "http://live.com",
        "document": "http://doc.com",
        "features": ["Feature 1"],
        "screenshots": ["http://image.com/screen1.png"],
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    with patch("app.api.admin.projects.verify_passkey") as mock_verify:
        with patch("app.api.admin.projects.ProjectRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.update_project.return_value = expected_response

            response = client.put(f"/admin/projects/{project_id}", json=payload)
            
            assert response.status_code == 200
            assert response.json() == expected_response
            mock_instance.update_project.assert_called_once()
            mock_verify.assert_called_once_with("secret")


def test_update_project_not_found():
    project_id = "nonexistent"
    payload = {
        "passkey": "secret",
        "name": "Updated Project"
    }

    with patch("app.api.admin.projects.verify_passkey") as mock_verify:
        with patch("app.api.admin.projects.ProjectRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.update_project.return_value = None

            response = client.put(f"/admin/projects/{project_id}", json=payload)
            
            assert response.status_code == 404
            assert response.json()["detail"] == "Project not found"

def test_delete_project_success():
    project_id = "123"
    payload = {"passkey": "secret"}

    with patch("app.api.admin.projects.verify_passkey") as mock_verify:
        with patch("app.api.admin.projects.ProjectRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.delete_project.return_value = True

            response = client.request("DELETE", f"/admin/projects/{project_id}", json=payload)
            
            assert response.status_code == 200
            assert response.json() == {"message": "Project deleted successfully"}
            mock_instance.delete_project.assert_called_once_with(project_id)
            mock_verify.assert_called_once_with("secret")
