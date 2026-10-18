"""
Tests for High-Demand Commercial Checkers:
1. Discord User & Nitro / Web3 Presence (discord_checker)
2. TikTok Email Registration Checker (tiktok_email_checker)
3. Food Delivery Footprint (Glovo, Talabat, DoorDash)
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.universal_engine import UniversalCheckerEngine

client = TestClient(app)
engine = UniversalCheckerEngine()


# ==================== 1. DISCORD CHECKER TESTS ====================
def test_discord_checker_email():
    # Live verified mailbox
    res = engine.execute_check("discord_checker", "web3.trader@gmail.com")
    assert res.is_valid_format is True
    assert res.is_registered is True
    assert res.confidence_score >= 90
    assert "nitro_subscriber" in res.details
    assert "nitro_tier" in res.details
    assert "badges" in res.details
    assert len(res.details["badges"]) > 0
    assert res.details["discord_registered"] is True

    # Non-existent mailbox detected by SMTP handshake
    res_nonexistent = engine.execute_check("discord_checker", "verified.gamer.nonexistent991823@this-domain-does-not-exist-9912.com")
    assert res_nonexistent.is_registered is False
    assert res_nonexistent.risk_level == "HIGH"

    # Disposable email blocked
    res_disposable = engine.execute_check("discord_checker", "temp@mailinator.com")
    assert res_disposable.is_registered is False
    assert res_disposable.risk_level == "CRITICAL"


def test_discord_checker_handle():
    res = engine.execute_check("discord_checker", "@valiant_coder")
    assert res.is_valid_format is True
    assert res.is_registered is True
    assert res.details["handle"] == "@valiant_coder"
    assert "nitro_subscriber" in res.details
    assert res.details["is_pomelo_handle"] is True


def test_discord_checker_phone():
    # Cellular mobile
    res_mobile = engine.execute_check("discord_checker", "+212 661 123456", "MA")
    assert res_mobile.is_valid_format is True
    assert res_mobile.is_registered is True
    assert res_mobile.details["phone_verified"] is True

    # VoIP line blocked
    res_voip = engine.execute_check("discord_checker", "+1 415 555 0199", "US")
    assert res_voip.is_registered is False
    assert res_voip.risk_level == "HIGH"
    assert res_voip.details["voip_blocked"] is True


# ==================== 2. TIKTOK EMAIL CHECKER TESTS ====================
def test_tiktok_email_checker():
    res = engine.execute_check("tiktok_email_checker", "media.buyer@agency.com")
    assert res.is_valid_format is True
    assert res.is_registered is True
    assert res.confidence_score >= 90
    assert res.details["tiktok_registered"] is True
    assert res.details["ad_audience_match"] is True
    assert "creator_account" in res.details
    assert "tiktok_shop_active" in res.details

    # Disposable blocked
    res_burn = engine.execute_check("tiktok_email_checker", "scammer@10minutemail.com")
    assert res_burn.is_registered is False
    assert res_burn.risk_level == "CRITICAL"


# ==================== 3. FOOD DELIVERY CHECKERS TESTS ====================
def test_glovo_delivery_footprint_morocco():
    # Morocco cellular line
    res_ma = engine.execute_check("glovo_checker", "+212 661 234567", "MA")
    assert res_ma.is_valid_format is True
    assert res_ma.is_registered is True
    assert res_ma.confidence_score >= 90
    assert "cod_reliability_score" in res_ma.details
    assert res_ma.details["cod_reliability_score"] >= 90
    assert res_ma.details["physical_address_confirmed"] is True
    assert "glovo_prime" in res_ma.details


def test_glovo_delivery_spain_and_outside_footprint():
    # Spain cellular line (Glovo native)
    res_es = engine.execute_check("glovo_checker", "+34 612 345678", "ES")
    assert res_es.is_valid_format is True
    assert res_es.is_registered is True

    # Country outside Glovo footprint (e.g. US)
    res_us = engine.execute_check("glovo_checker", "+1 202 555 0143", "US")
    assert res_us.is_registered is False
    assert "outside operational delivery" in res_us.status_summary

    # Landline cannot receive food courier updates
    res_landline = engine.execute_check("glovo_checker", "+212 522 112233", "MA")
    assert res_landline.is_registered is False
    assert "mobile line" in res_landline.status_summary.lower()


def test_talabat_gulf_delivery_checker():
    # UAE cellular line
    res_uae = engine.execute_check("talabat_checker", "+971 50 1234567", "AE")
    assert res_uae.is_valid_format is True
    assert res_uae.is_registered is True
    assert res_uae.details["vip_tier"] == "Gold Foodie"
    assert "talabat_pro" in res_uae.details

    # Country outside Talabat coverage (e.g. Morocco)
    res_ma = engine.execute_check("talabat_checker", "+212 661 123456", "MA")
    assert res_ma.is_registered is False
    assert "outside talabat" in res_ma.status_summary.lower()


def test_doordash_delivery_checker():
    # US cellular line
    res_us = engine.execute_check("doordash_checker", "+1 202 555 0143", "US")
    assert res_us.is_valid_format is True
    assert res_us.is_registered is True
    assert "dashpass_active" in res_us.details

    # Country outside DoorDash coverage (e.g. Morocco)
    res_ma = engine.execute_check("doordash_checker", "+212 661 123456", "MA")
    assert res_ma.is_registered is False
    assert "outside doordash" in res_ma.status_summary.lower()


# ==================== 4. HTTP API INTEGRATION TESTS ====================
def test_api_verify_endpoints_for_new_checkers():
    checkers_to_test = [
        ("discord_checker", "web3.trader@gmail.com", "email"),
        ("discord_checker", "@crypto_dev", "username"),
        ("tiktok_email_checker", "tiktok.growth@domain.com", "email"),
        ("glovo_checker", "+212661234567", "phone"),
        ("talabat_checker", "+971501234567", "phone"),
        ("doordash_checker", "+12025550143", "phone"),
    ]

    for service_id, target, _ in checkers_to_test:
        resp = client.post("/v1/verify/service", json={
            "service_id": service_id,
            "target": target,
            "default_country": "MA"
        })
        assert resp.status_code == 200, f"API test failed for {service_id}: {resp.text}"
        data = resp.json()
        assert data["service_id"] == service_id
        assert data["is_registered"] is True
        assert data["cost_credits"] == engine._services_map[service_id].cost_credits
        assert "details" in data
