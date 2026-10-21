"""
Unit and Integration Tests for Email Verification Flow.
ECC Standards: Immutability, Error Handling, Security.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import DatabaseService
from app.core.auth import AuthService

client = TestClient(app)
db = DatabaseService()
auth_service = AuthService(db=db)


def test_registration_and_email_verification_lifecycle():
    email = "test_verified_user_99@company.com"
    password = "SecurePassword123!"
    full_name = "Verification Test Candidate"

    # Clean up test user if exists from prior runs
    with db.get_connection() as conn:
        cursor = db.get_cursor(conn)
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))

    # 1. Register user
    reg_res = client.post("/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": full_name
    })
    assert reg_res.status_code == 200, reg_res.text
    data = reg_res.json()
    assert data["user"]["email"] == email
    assert data["user"]["email_verified"] is False

    # Get verification token directly from DB
    with db.get_connection() as conn:
        cursor = db.get_cursor(conn)
        cursor.execute("SELECT id, verification_token, email_verified FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        assert row is not None
        user_id = row["id"]
        token = row["verification_token"]
        assert token is not None
        assert row["email_verified"] == 0

    # 2. Test invalid verification token
    bad_res = client.get("/v1/auth/verify-email?token=invalid_dummy_token_123")
    assert bad_res.status_code == 400
    assert "invalid" in bad_res.json()["detail"].lower()

    # 3. Verify with valid token
    verify_res = client.get(f"/v1/auth/verify-email?token={token}")
    assert verify_res.status_code == 200
    verify_data = verify_res.json()
    assert verify_data["success"] is True
    assert verify_data["user"]["email_verified"] is True

    # 4. Check DB state: token should be cleared and email_verified=1
    with db.get_connection() as conn:
        cursor = db.get_cursor(conn)
        cursor.execute("SELECT verification_token, email_verified FROM users WHERE id = ?", (user_id,))
        row_after = cursor.fetchone()
        assert row_after["verification_token"] is None
        assert row_after["email_verified"] == 1

    # 5. Token reuse should fail
    reuse_res = client.get(f"/v1/auth/verify-email?token={token}")
    assert reuse_res.status_code == 400

    # 6. Admin user list should report email_verified=True
    admin_res = client.get("/v1/admin/users", headers={"X-Admin-Key": "checkerleak_admin_master_2025"})
    assert admin_res.status_code == 200
    admin_users = admin_res.json()["users"]
    target_admin_u = next((u for u in admin_users if u["email"] == email), None)
    assert target_admin_u is not None
    assert target_admin_u["email_verified"] is True

    # 7. Admin manual override: toggle unverify and re-verify
    override_res = client.post(
        f"/v1/admin/users/{user_id}/verify-email",
        headers={"X-Admin-Key": "checkerleak_admin_master_2025"},
        json={"verified": False}
    )
    assert override_res.status_code == 200
    assert override_res.json()["email_verified"] is False

    reverify_res = client.post(
        f"/v1/admin/users/{user_id}/verify-email",
        headers={"X-Admin-Key": "checkerleak_admin_master_2025"},
        json={"verified": True}
    )
    assert reverify_res.status_code == 200
    assert reverify_res.json()["email_verified"] is True
