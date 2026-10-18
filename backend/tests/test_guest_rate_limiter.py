"""
Unit and Integration tests for Guest Rate Limiter and Free Trial Quotas - TDD
Validates 3 free checks per IP per 24 hours, HTTP 429 responses, quota endpoint, and authenticated bypass.
"""
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.rate_limiter import GuestRateLimiter
from app.core.auth import AuthService

client = TestClient(app)
auth_service = AuthService()


def test_rate_limiter_unit_logic():
    """Unit test for GuestRateLimiter sliding window and IP isolation."""
    limiter = GuestRateLimiter(max_free_checks=3, window_seconds=86400)
    test_ip = "192.168.1.100"

    # Check 0: 3 remaining
    allowed, remaining, max_c = limiter.check_guest_limit(test_ip)
    assert allowed is True
    assert remaining == 3
    assert max_c == 3

    # Check 1
    rem1 = limiter.record_guest_check(test_ip)
    assert rem1 == 2
    assert limiter.get_remaining(test_ip) == 2

    # Check 2
    rem2 = limiter.record_guest_check(test_ip)
    assert rem2 == 1

    # Check 3
    rem3 = limiter.record_guest_check(test_ip)
    assert rem3 == 0

    # Check 4: Blocked!
    allowed, remaining, _ = limiter.check_guest_limit(test_ip)
    assert allowed is False
    assert remaining == 0

    # Independent IP has full quota
    other_ip = "10.0.0.1"
    allowed_other, rem_other, _ = limiter.check_guest_limit(other_ip)
    assert allowed_other is True
    assert rem_other == 3

    # Reset IP
    limiter.reset_ip(test_ip)
    allowed_reset, rem_reset, _ = limiter.check_guest_limit(test_ip)
    assert allowed_reset is True
    assert rem_reset == 3


def test_guest_quota_endpoint():
    """Test GET /v1/guest/quota returns quota details."""
    test_ip = f"172.16.{uuid.uuid4().int % 250}.{uuid.uuid4().int % 250}"
    headers = {"X-Forwarded-For": test_ip}

    resp = client.get("/v1/guest/quota", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["client_ip"] == test_ip
    assert data["remaining"] == 3
    assert data["max_free_checks"] == 3
    assert data["allowed"] is True


def test_guest_verify_service_rate_limit_enforcement():
    """Verify that a guest IP can perform exactly 3 free checks and the 4th returns 429."""
    guest_ip = f"198.51.100.{uuid.uuid4().int % 250}"
    headers = {"X-Forwarded-For": guest_ip}

    payload = {
        "service_id": "phone_validation",
        "target": "+212 661 112233",
        "default_country": "MA",
    }

    # 1st free check -> 200
    r1 = client.post("/v1/verify/service", json=payload, headers=headers)
    assert r1.status_code == 200

    # Check quota -> 2 remaining
    q1 = client.get("/v1/guest/quota", headers=headers).json()
    assert q1["remaining"] == 2

    # 2nd free check -> 200
    r2 = client.post("/v1/verify/service", json=payload, headers=headers)
    assert r2.status_code == 200

    # 3rd free check -> 200
    r3 = client.post("/v1/verify/service", json=payload, headers=headers)
    assert r3.status_code == 200

    # 4th check -> 429 Too Many Requests
    r4 = client.post("/v1/verify/service", json=payload, headers=headers)
    assert r4.status_code == 429
    detail = r4.json()["detail"]
    assert "FREE_TRIAL_LIMIT_REACHED" in detail
    assert "Please sign in or top up" in detail


def test_guest_verify_single_rate_limit_enforcement():
    """Verify rate limit enforcement on /v1/verify/single endpoint."""
    guest_ip = f"203.0.113.{uuid.uuid4().int % 250}"
    headers = {"X-Forwarded-For": guest_ip}

    payload = {
        "phone": "+212 661 445566",
        "check_whatsapp": True,
    }

    # Use all 3 checks
    for _ in range(3):
        res = client.post("/v1/verify/single", json=payload, headers=headers)
        assert res.status_code == 200

    # 4th check fails with 429
    res_blocked = client.post("/v1/verify/single", json=payload, headers=headers)
    assert res_blocked.status_code == 429
    assert "FREE_TRIAL_LIMIT_REACHED" in res_blocked.json()["detail"]


def test_authenticated_user_bypasses_guest_rate_limit():
    """Verify that an authenticated user with credits is not blocked by guest rate limit."""
    guest_ip = f"198.51.100.{uuid.uuid4().int % 250}"
    headers = {"X-Forwarded-For": guest_ip}

    # Drain guest quota to 0
    payload = {"service_id": "phone_validation", "target": "+212661000000"}
    for _ in range(3):
        client.post("/v1/verify/service", json=payload, headers=headers)

    # Guest is now blocked
    blocked = client.post("/v1/verify/service", json=payload, headers=headers)
    assert blocked.status_code == 429

    # Now create authenticated user and add credits
    user = auth_service.register(f"auth_bypass_{uuid.uuid4().hex[:6]}@agency.io", "Pass12345!", "Auth Tester")
    auth_service.add_credits(user.id, 50)

    # Authenticated user can verify from the exact same IP!
    authed_payload = {
        "service_id": "phone_validation",
        "target": "+212661000000",
        "user_id": user.id,
    }
    authed_res = client.post("/v1/verify/service", json=authed_payload, headers=headers)
    assert authed_res.status_code == 200
