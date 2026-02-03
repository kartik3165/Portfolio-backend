import os

def test_update_bio_success(client, mock_dynamo_table):
    os.environ["PASSKEY"] = "secret"
    mock_dynamo_table.put_item.return_value = {}
    
    payload = {
        "summary": "Sum",
        "highlights": ["H1"],
        "about_intro": "Intro",
        "story": "Story",
        "passkey": "secret"
    }
    
    response = client.put("/admin/bio", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_update_bio_unauthorized(client, mock_dynamo_table):
    os.environ["PASSKEY"] = "secret"
    
    payload = {
        "summary": "Sum",
        "highlights": ["H1"],
        "about_intro": "Intro",
        "story": "Story",
        "passkey": "wrong"
    }
    
    response = client.put("/admin/bio", json=payload)
    assert response.status_code == 401
