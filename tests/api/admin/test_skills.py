from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app

client = TestClient(app)

def test_add_skill_success():
    payload = {
        "passkey": "test_passkey",
        "skill": "Python"
    }
    mock_response = {"skills": ["Python"]}

    with patch("app.api.admin.skills.verify_passkey") as mock_verify:
        with patch("app.api.admin.skills.SkillsRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.add_skill.return_value = mock_response

            response = client.post("/admin/skill/add", json=payload)
            
            assert response.status_code == 200
            assert response.json() == mock_response
            mock_verify.assert_called_once_with("test_passkey")
            mock_instance.add_skill.assert_called_once_with("Python")

def test_add_skill_invalid_passkey():
    payload = {
        "passkey": "wrong_passkey",
        "skill": "Python"
    }
    
    with patch("app.api.admin.skills.verify_passkey") as mock_verify:
        mock_verify.side_effect = HTTPException(status_code=401, detail="Invalid passkey")
        
        response = client.post("/admin/skill/add", json=payload)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid passkey"

def test_remove_skill_success():
    payload = {
        "passkey": "test_passkey",
        "skill": "Python"
    }
    mock_response = {"skills": []}

    with patch("app.api.admin.skills.verify_passkey") as mock_verify:
        with patch("app.api.admin.skills.SkillsRepo") as MockRepo:
            mock_instance = MockRepo.return_value
            mock_instance.remove_skill.return_value = mock_response

            response = client.post("/admin/skill/remove", json=payload)
            
            assert response.status_code == 200
            assert response.json() == mock_response
            mock_verify.assert_called_once_with("test_passkey")
            mock_instance.remove_skill.assert_called_once_with("Python")
