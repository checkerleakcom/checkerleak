"""
Unit and Integration tests for Developer API Key rotation and code snippet generation.
"""
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import AuthService

client = TestClient(app)
auth_service = AuthService()


def test_developer_key_rotation_and_snippets():
    unique_email = f"dev_tester_{uuid.uuid4().hex[:8]}@pulsecheck.com"
    user = auth_service.register(unique_email, "pass12345", "Dev Tester")
    old_key = user.api_key

    # 1. Rotate API Key
    resp = client.post("/v1/developer/regenerate-key", json={"user_id": user.id})
    assert resp.status_code == 200
    data = resp.json()
    new_key = data["new_api_key"]
    assert new_key.startswith("pulse_live_")
    assert new_key != old_key

    # 2. Fetch code snippets
    resp_snip = client.get(f"/v1/developer/snippets?user_id={user.id}&target_sample=+212661234567")
    assert resp_snip.status_code == 200
    snip_data = resp_snip.json()
    assert snip_data["api_key"] == new_key
    assert "curl" in snip_data["snippets"]
    assert "python" in snip_data["snippets"]
    assert "javascript" in snip_data["snippets"]
    assert new_key in snip_data["snippets"]["curl"]
    assert new_key in snip_data["snippets"]["python"]
