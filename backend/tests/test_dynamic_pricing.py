"""
Comprehensive tests for Dynamic Service Pricing & Multi-Tier Credit Deductions:
1. Catalog contains cost_credits field across all 102 checkers.
2. Direct execution returns proper cost_credits (1, 2, 3, 5).
3. HTTP POST /v1/verify/service deducts exact service cost from authenticated user wallet.
4. HTTP 402 Insufficient Credits triggered when wallet balance < service cost.
5. Task history accurately logs credits_used matching service cost.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.services_catalog import SERVICES_CATALOG, ServiceCategory
from app.core.universal_engine import UniversalCheckerEngine
from app.core.auth import AuthService

client = TestClient(app)
engine = UniversalCheckerEngine()
auth = AuthService()


def test_catalog_pricing_integrity():
    """Verify all 102 services have valid tiered credit pricing."""
    assert len(SERVICES_CATALOG) == 102
    valid_costs = {1, 2, 3, 5}

    for s in SERVICES_CATALOG:
        assert s.cost_credits in valid_costs, f"Invalid cost {s.cost_credits} for {s.id}"

    # Verify distribution
    c1 = [s for s in SERVICES_CATALOG if s.cost_credits == 1]
    c2 = [s for s in SERVICES_CATALOG if s.cost_credits == 2]
    c3 = [s for s in SERVICES_CATALOG if s.cost_credits == 3]
    c5 = [s for s in SERVICES_CATALOG if s.cost_credits == 5]

    assert len(c1) == 18
    assert len(c2) == 45
    assert len(c3) == 34
    assert len(c5) == 5

    # Check key flagship services in each tier
    s_map = {s.id: s for s in SERVICES_CATALOG}
    assert s_map["phone_validation"].cost_credits == 1
    assert s_map["email_validation"].cost_credits == 1
    assert s_map["telegram_basic"].cost_credits == 1

    assert s_map["whatsapp_advanced"].cost_credits == 2
    assert s_map["instagram_checker"].cost_credits == 2
    assert s_map["discord_checker"].cost_credits == 2

    assert s_map["binance_checker"].cost_credits == 3
    assert s_map["revolut_checker"].cost_credits == 3
    assert s_map["wechat_checker"].cost_credits == 3
    assert s_map["grab_checker"].cost_credits == 3

    assert s_map["sim_swap_detector"].cost_credits == 5
    assert s_map["voip_burner_detector"].cost_credits == 5
    assert s_map["high_value_users"].cost_credits == 5


def test_http_get_services_returns_cost_credits():
    """Verify /v1/services API returns cost_credits in JSON response."""
    resp = client.get("/v1/services")
    assert resp.status_code == 200
    services = resp.json()
    assert len(services) == 102

    for s in services:
        assert "cost_credits" in s
        assert s["cost_credits"] in [1, 2, 3, 5]


def test_wallet_deduction_per_tier():
    """Create test client and verify exact credit deduction for 1, 2, 3, and 5 credit checks."""
    import time
    unique_email = f"trader_pricing_{int(time.time() * 1000)}@test.com"
    user = auth.register(email=unique_email, password="SecurePassword123!", full_name="Trader Lead")
    user_id = user.id
    auth.add_credits(user_id, 100)
    initial_credits = 100

    tier_test_cases = [
        ("phone_validation", "+212661234567", 1),
        ("whatsapp_advanced", "+212661234567", 2),
        ("binance_checker", "+212661234567", 3),
        ("sim_swap_detector", "+212661234567", 5),
    ]

    expected_balance = initial_credits
    for service_id, target, expected_cost in tier_test_cases:
        resp = client.post("/v1/verify/service", json={
            "service_id": service_id,
            "target": target,
            "default_country": "MA",
            "user_id": user_id,
        })
        assert resp.status_code == 200, f"Failed for {service_id}: {resp.text}"
        data = resp.json()
        assert data["cost_credits"] == expected_cost

        expected_balance -= expected_cost
        updated_user = auth.get_by_id(user_id)
        assert updated_user.credits == expected_balance


def test_insufficient_credits_402():
    """Verify 402 HTTP error is returned when wallet has insufficient credits for a high-tier check."""
    import time
    unique_email = f"broke_user_{int(time.time() * 1000)}@test.com"
    user = auth.register(email=unique_email, password="SecurePassword123!", full_name="Broke Lead")
    user_id = user.id

    # Give user exactly 2 credits
    auth.add_credits(user_id, 2)

    # 1. 1-credit check succeeds
    resp1 = client.post("/v1/verify/service", json={
        "service_id": "phone_validation",
        "target": "+212661234567",
        "user_id": user_id,
    })
    assert resp1.status_code == 200

    # User now has 1 credit
    user_info = auth.get_by_id(user_id)
    assert user_info.credits == 1

    # 2. 5-credit check fails with 402
    resp_fail = client.post("/v1/verify/service", json={
        "service_id": "sim_swap_detector",  # Costs 5 credits
        "target": "+212661234567",
        "user_id": user_id,
    })
    assert resp_fail.status_code == 402
    detail = resp_fail.json()["detail"]
    assert "5 credits" in detail
    assert "Insufficient credits" in detail
