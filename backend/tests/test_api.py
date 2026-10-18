"""
Test suite for FastAPI Verification API - TDD
Validates REST endpoints, request payloads, API security headers, and batch processing.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_dashboard_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "CheckerLeak.com" in response.text
    assert "CheckerLeak" in response.text


def test_health_check_endpoint():
    response = client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "IMESSAGE" in data["supported_channels"]


def test_single_verify_endpoint_success():
    payload = {
        "phone": "+212 661 123456",
        "check_whatsapp": True,
        "check_telegram": True,
        "check_imessage": True,
        "check_rcs": True,
        "check_social": True,
        "check_crypto": True,
    }
    response = client.post("/v1/verify/single", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True
    assert data["phone"]["e164"] == "+212661123456"
    assert data["imessage"] is not None
    assert data["rcs"] is not None
    assert data["social"] is not None
    assert data["crypto"] is not None
    assert data["reachability_score"] >= 80
    assert data["lead_quality"] in ["EXCELLENT", "HIGH"]


def test_single_verify_endpoint_invalid_number():
    payload = {
        "phone": "invalid_num_123",
        "check_whatsapp": True,
    }
    response = client.post("/v1/verify/single", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False
    assert data["reachability_score"] == 0
    assert data["lead_quality"] == "DEAD"


def test_batch_verify_endpoint():
    payload = {
        "numbers": ["+212 661 111111", "+1 (415) 555-2671", "invalid"],
        "check_whatsapp": True,
        "check_imessage": True,
    }
    response = client.post("/v1/verify/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["valid_count"] == 2
    assert data["invalid_count"] == 1
    assert len(data["results"]) == 3


def test_auth_register_and_login_flow():
    import uuid
    unique_email = f"client_{uuid.uuid4().hex[:8]}@agency.io"

    # 1. Register
    reg_resp = client.post(
        "/v1/auth/register",
        json={"email": unique_email, "password": "SecretPassword123!", "full_name": "Test Agency"},
    )
    assert reg_resp.status_code == 200
    reg_data = reg_resp.json()
    assert reg_data["user"]["email"] == unique_email
    assert reg_data["user"]["credits"] == 0
    assert reg_data["user"]["api_key"].startswith("pk_live_")
    user_id = reg_data["user"]["id"]

    # 2. Login
    login_resp = client.post(
        "/v1/auth/login",
        json={"email": unique_email, "password": "SecretPassword123!"},
    )
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["user"]["id"] == user_id
    assert login_data["user"]["credits"] == 0

    # 3. Get profile /me
    me_resp = client.get(f"/v1/auth/me?user_id={user_id}")
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["full_name"] == "Test Agency"
    assert me_data["credits"] == 0

    # 3b. Top up user with credits for verification
    from app.core.auth import AuthService
    AuthService().add_credits(user_id, 10)

    # 4. Verify Single with user_id -> should deduct 1 credit and log history
    v_resp = client.post(
        "/v1/verify/single",
        json={"phone": "+212 661 999999", "check_whatsapp": True, "user_id": user_id},
    )
    assert v_resp.status_code == 200

    # 5. Check balance is now 9
    me_after = client.get(f"/v1/auth/me?user_id={user_id}").json()
    assert me_after["credits"] == 9

    # 6. Check task history
    hist_resp = client.get(f"/v1/tasks/history?user_id={user_id}&limit=10")
    assert hist_resp.status_code == 200
    history = hist_resp.json()
    assert len(history) >= 1
    assert history[0]["phone"] == "+212661999999"
    assert history[0]["credits_used"] == 1


def test_auth_login_invalid_password():
    response = client.post(
        "/v1/auth/login",
        json={"email": "nonexistent@agency.io", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
