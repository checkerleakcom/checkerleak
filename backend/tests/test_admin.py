"""
Test Suite for CheckerLeak Admin Command Center
Validates authentication guards, executive stats, credit balance adjustments,
account bans, transaction approvals, telemetry, and audit logs.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import DatabaseService
from app.api.admin_router import ADMIN_SECRET_KEY

client = TestClient(app)
db_service = DatabaseService()


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Ensure clean slate before tests run."""
    with db_service.get_connection() as conn:
        cursor = db_service.get_cursor(conn)
        cursor.execute("DELETE FROM admin_audit_logs")
        cursor.execute("DELETE FROM billing_transactions WHERE user_id IN (SELECT id FROM users WHERE email LIKE 'admin_test_%')")
        cursor.execute("DELETE FROM task_history WHERE user_id IN (SELECT id FROM users WHERE email LIKE 'admin_test_%')")
        cursor.execute("DELETE FROM users WHERE email LIKE 'admin_test_%'")
    yield


def create_test_user(email="admin_test_user@example.com", credits=1000):
    with db_service.get_connection() as conn:
        cursor = db_service.get_cursor(conn)
        cursor.execute("""
            INSERT INTO users (email, password_hash, salt, full_name, credits, api_key, status)
            VALUES (?, 'dummy_hash', 'dummy_salt', 'Admin Test Subject', ?, ?, 'active')
        """, (email, credits, f"api_key_{email}"))
        cursor.execute("SELECT id, email, credits, status FROM users WHERE email = ?", (email,))
        return cursor.fetchone()


def test_admin_auth_unauthorized():
    """Requests without token must be rejected with 401."""
    res = client.get("/v1/admin/stats")
    assert res.status_code == 401


def test_admin_auth_invalid_key():
    """Requests with wrong key must be rejected with 403."""
    res = client.get("/v1/admin/stats", headers={"X-Admin-Key": "completely_wrong_key"})
    assert res.status_code == 403


def test_admin_login_success():
    """Correct secret must yield 200 and return token."""
    res = client.post("/v1/admin/login", json={"secret_key": ADMIN_SECRET_KEY})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["token"] == ADMIN_SECRET_KEY


def test_admin_login_failure():
    """Wrong secret must yield 401."""
    res = client.post("/v1/admin/login", json={"secret_key": "wrong_password"})
    assert res.status_code == 401


def test_admin_stats_overview():
    """Stats endpoint returns structured executive KPIs."""
    res = client.get("/v1/admin/stats", headers={"X-Admin-Key": ADMIN_SECRET_KEY})
    assert res.status_code == 200
    data = res.json()
    assert "revenue" in data
    assert "users" in data
    assert "verifications" in data
    assert "system" in data
    assert data["verifications"]["engines_active"] == 102


def test_admin_users_pagination_and_search():
    """Users endpoint lists accounts and supports search."""
    user = create_test_user("admin_test_searchable@example.com", credits=500)
    res = client.get("/v1/admin/users?search=searchable", headers={"X-Admin-Key": ADMIN_SECRET_KEY})
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    found = any(u["email"] == "admin_test_searchable@example.com" for u in data["users"])
    assert found is True


def test_adjust_user_credits_atomic():
    """Admin can atomically add or deduct credits with an audit trail."""
    user = create_test_user("admin_test_credit@example.com", credits=500)
    user_id = user["id"]

    # Add 2,500 credits
    res = client.post(
        f"/v1/admin/users/{user_id}/adjust-credits",
        headers={"X-Admin-Key": ADMIN_SECRET_KEY},
        json={"delta_credits": 2500, "reason": "VIP Client Top-Up Goodwill"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["new_credits"] == 3000
    assert data["delta"] == 2500

    # Verify audit log was recorded
    audit_res = client.get("/v1/admin/audit-logs", headers={"X-Admin-Key": ADMIN_SECRET_KEY})
    assert audit_res.status_code == 200
    logs = audit_res.json()["logs"]
    assert any("VIP Client Top-Up" in l["details"] for l in logs)


def test_toggle_user_status_ban_and_unban():
    """Admin can toggle user between active and banned."""
    user = create_test_user("admin_test_ban@example.com", credits=100)
    user_id = user["id"]

    # Ban
    res = client.post(
        f"/v1/admin/users/{user_id}/toggle-status",
        headers={"X-Admin-Key": ADMIN_SECRET_KEY},
        json={"status": "banned"}
    )
    assert res.status_code == 200
    assert res.json()["status"] == "banned"

    # Unban
    res2 = client.post(
        f"/v1/admin/users/{user_id}/toggle-status",
        headers={"X-Admin-Key": ADMIN_SECRET_KEY},
        json={"status": "active"}
    )
    assert res2.status_code == 200
    assert res2.json()["status"] == "active"


def test_override_confirm_transaction():
    """Admin can manually approve and credit a pending crypto deposit."""
    user = create_test_user("admin_test_deposit@example.com", credits=200)
    user_id = user["id"]

    # Insert pending deposit
    with db_service.get_connection() as conn:
        cursor = db_service.get_cursor(conn)
        cursor.execute("""
            INSERT INTO billing_transactions (user_id, plan_id, amount_usd, credits_added, payment_method, status, tx_hash)
            VALUES (?, 'STARTER', 15.00, 1500, 'BTC', 'PENDING', '0x_test_hash_override_123')
        """, (user_id,))
        cursor.execute("SELECT id FROM billing_transactions WHERE tx_hash = '0x_test_hash_override_123'")
        tx_id = cursor.fetchone()["id"]

    # Call override confirm
    res = client.post(
        f"/v1/admin/transactions/{tx_id}/override-confirm",
        headers={"X-Admin-Key": ADMIN_SECRET_KEY},
        json={"admin_note": "Manual confirmation from mempool listener"}
    )
    assert res.status_code == 200
    assert res.json()["status"] == "COMPLETED"

    # Verify user credits increased by 1500 (200 + 1500 = 1700)
    with db_service.get_connection() as conn:
        cursor = db_service.get_cursor(conn)
        cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
        updated_user = cursor.fetchone()
        assert updated_user["credits"] == 1700


def test_telemetry_endpoint():
    """Telemetry returns cluster and engine stats for all 102 checkers."""
    res = client.get("/v1/admin/telemetry", headers={"X-Admin-Key": ADMIN_SECRET_KEY})
    assert res.status_code == 200
    data = res.json()
    assert data["fleet_total"] == 102
    assert len(data["categories"]) == 4
    assert len(data["top_engines"]) > 0
