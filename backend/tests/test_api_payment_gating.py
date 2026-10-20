"""
Test Suite for Strict Commercial API Payment Gating
Ensures that no external API, SDK, or automated caller can access verification engines
without an active API key and paid credit balance.
"""
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import DatabaseService

client = TestClient(app)
db = DatabaseService()


def create_api_user(email="api_payer@test.com", credits=10):
    with db.get_connection() as conn:
        cursor = db.get_cursor(conn)
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        cursor.execute("""
            INSERT INTO users (email, password_hash, salt, full_name, credits, api_key, status)
            VALUES (?, 'pwd_hash', 'salt', 'Payer User', ?, ?, 'active')
        """, (email, credits, f"api_test_key_{email}"))
        cursor.execute("SELECT id, email, credits, api_key FROM users WHERE email = ?", (email,))
        return cursor.fetchone()


def test_external_api_caller_without_key_is_blocked():
    """External API callers (e.g. Python, Node, cURL) without API key are rejected with 401."""
    res = client.post(
        "/v1/verify/single",
        json={"phone": "+12025550199"},
        headers={"User-Agent": "python-requests/2.31.0"}
    )
    assert res.status_code == 401
    assert "API_KEY_AND_PAYMENT_REQUIRED" in res.json()["detail"]


def test_external_api_caller_with_invalid_key():
    """Callers with an invalid or non-existent API key are rejected with 401."""
    res = client.post(
        "/v1/verify/single",
        json={"phone": "+12025550199"},
        headers={"X-API-Key": "pk_live_completely_fake_key_12345", "User-Agent": "checkerleak-sdk"}
    )
    assert res.status_code == 401
    assert "INVALID_API_KEY" in res.json()["detail"]


def test_external_api_caller_with_zero_credits_blocked():
    """Callers with 0 credits are blocked with 402 Payment Required."""
    user = create_api_user("broke_api_client@test.com", credits=0)
    api_key = user["api_key"]

    res = client.post(
        "/v1/verify/single",
        json={"phone": "+12025550199"},
        headers={"X-API-Key": api_key, "User-Agent": "checkerleak-sdk"}
    )
    assert res.status_code == 402
    assert "PAYMENT_REQUIRED" in res.json()["detail"]


def test_external_api_caller_with_paid_credits_succeeds_and_deducts():
    """Callers with paid credits succeed and have their credits deducted atomically."""
    user = create_api_user("paid_api_client@test.com", credits=5)
    api_key = user["api_key"]
    user_id = user["id"]

    res = client.post(
        "/v1/verify/single",
        json={"phone": "+12025550199"},
        headers={"X-API-Key": api_key, "User-Agent": "checkerleak-sdk"}
    )
    assert res.status_code == 200
    assert res.json()["is_valid"] is True

    # Verify credit deducted in DB (5 - 1 = 4)
    with db.get_connection() as conn:
        cursor = db.get_cursor(conn)
        cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
        updated = cursor.fetchone()
        assert updated["credits"] == 4
