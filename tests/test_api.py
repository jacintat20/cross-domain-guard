from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_unauthorized_access():
    response = client.post("/api/v1/transfer", json={"destination_domain": "SECRET", "classification": "UNCLASS", "content": "Test"})
    assert response.status_code == 401

def test_high_to_low_rejection():
    headers = {"x-api-key": "key-user-secret"}
    payload = {
        "destination_domain": "UNCLASS",
        "classification": "SECRET",
        "content": "Classified Intelligence"
    }
    response = client.post("/api/v1/transfer", json=payload, headers=headers)
    assert response.status_code == 400
    assert "High-to-Low transfer prohibited" in response.json()["detail"]