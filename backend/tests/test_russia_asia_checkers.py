"""
Unit and Integration Tests for Russia (CIS) & Asia Power Engines:
1. Avito Russia Classifieds (avito_checker)
2. Odnoklassniki (okru_checker)
3. KakaoTalk & KakaoPay (kakaotalk_checker)
4. WeChat China Real-Name (wechat_checker)
5. Grab Southeast Asia Super-App (grab_checker)
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.universal_engine import UniversalCheckerEngine

client = TestClient(app)
engine = UniversalCheckerEngine()


# ==================== 1. AVITO RUSSIA CHECKER ====================
def test_avito_phone_russia_and_cis():
    # Russia mobile (+7916...)
    res_ru = engine.execute_check("avito_checker", "+7 916 123 4567", "RU")
    assert res_ru.is_valid_format is True
    assert res_ru.is_registered is True
    assert res_ru.confidence_score >= 90
    assert "is_seller" in res_ru.details
    assert "seller_rating" in res_ru.details
    assert "city" in res_ru.details

    # Landline cannot receive Avito SMS OTP
    res_landline = engine.execute_check("avito_checker", "+7 495 123 4567", "RU")
    assert res_landline.is_registered is False
    assert "cellular mobile" in res_landline.status_summary.lower()

    # VoIP line blocked
    res_voip = engine.execute_check("avito_checker", "+1 415 555 0199", "US")
    assert res_voip.is_registered is False
    assert res_voip.risk_level == "HIGH"

    # Outside Russia/CIS footprint
    res_outside = engine.execute_check("avito_checker", "+212 661 123456", "MA")
    assert res_outside.is_registered is False
    assert "outside russian" in res_outside.status_summary.lower()


# ==================== 2. ODNOKLASSNIKI (OK.RU) CHECKER ====================
def test_okru_phone_and_email():
    # Russia mobile
    res_phone = engine.execute_check("okru_checker", "+7 916 123 4567", "RU")
    assert res_phone.is_valid_format is True
    assert res_phone.is_registered is True
    assert "age_bracket" in res_phone.details
    assert "inferred_gender" in res_phone.details

    # Deliverable email
    res_email = engine.execute_check("okru_checker", "web3.trader@gmail.com")
    assert res_email.is_valid_format is True
    assert res_email.is_registered is True
    assert "age_bracket" in res_email.details

    # Disposable email blocked
    res_burn = engine.execute_check("okru_checker", "spam@mailinator.com")
    assert res_burn.is_registered is False
    assert res_burn.risk_level == "CRITICAL"


# ==================== 3. KAKAOTALK & KAKAOPAY CHECKER ====================
def test_kakaotalk_korea_and_hybrid():
    # South Korea mobile (+8210...)
    res_kr = engine.execute_check("kakaotalk_checker", "+82 10 1234 5678", "KR")
    assert res_kr.is_valid_format is True
    assert res_kr.is_registered is True
    assert res_kr.confidence_score >= 95
    assert "kakaopay_active" in res_kr.details
    assert res_kr.details["korean_telecom_ci_verified"] is True

    # Korean landline incompatible
    res_landline = engine.execute_check("kakaotalk_checker", "+82 2 123 4567", "KR")
    assert res_landline.is_registered is False

    # Kakao ID handle
    res_handle = engine.execute_check("kakaotalk_checker", "@seoul_trader")
    assert res_handle.is_valid_format is True
    assert res_handle.is_registered is True
    assert res_handle.details["kakao_id"] == "seoul_trader"

    # Kakao email
    res_email = engine.execute_check("kakaotalk_checker", "web3.trader@gmail.com")
    assert res_email.is_valid_format is True
    assert res_email.is_registered is True
    assert "kakaopay_ready" in res_email.details


# ==================== 4. WECHAT REAL-NAME CHECKER ====================
def test_wechat_china_and_id():
    # China mobile (+86138...)
    res_cn = engine.execute_check("wechat_checker", "+86 138 0013 8000", "CN")
    assert res_cn.is_valid_format is True
    assert res_cn.is_registered is True
    assert res_cn.confidence_score >= 95
    assert res_cn.details["real_name_verified"] is True
    assert res_cn.details["wechat_pay_ready"] is True

    # WeChat ID handle
    res_id = engine.execute_check("wechat_checker", "@shenzhen_supply")
    assert res_id.is_valid_format is True
    assert res_id.is_registered is True
    assert res_id.details["wechat_id"] == "shenzhen_supply"


# ==================== 5. GRAB SE ASIA CHECKER ====================
def test_grab_southeast_asia():
    # Singapore mobile (+65)
    res_sg = engine.execute_check("grab_checker", "+65 9123 4567", "SG")
    assert res_sg.is_valid_format is True
    assert res_sg.is_registered is True
    assert res_sg.confidence_score >= 90
    assert "grabrewards_tier" in res_sg.details
    assert "grabpay_active" in res_sg.details

    # Indonesia mobile (+62)
    res_id = engine.execute_check("grab_checker", "+62 812 3456 7890", "ID")
    assert res_id.is_valid_format is True
    assert res_id.is_registered is True

    # Outside SE Asia footprint (Morocco)
    res_ma = engine.execute_check("grab_checker", "+212 661 123456", "MA")
    assert res_ma.is_registered is False
    assert "outside grab" in res_ma.status_summary.lower()


# ==================== 6. HTTP API CONTRACTS AUDIT ====================
def test_http_api_endpoints_russia_asia():
    checks = [
        ("avito_checker", "+79161234567", "RU"),
        ("okru_checker", "+79161234567", "RU"),
        ("okru_checker", "web3.trader@gmail.com", "RU"),
        ("kakaotalk_checker", "+821012345678", "KR"),
        ("kakaotalk_checker", "@busan_buyer", "KR"),
        ("wechat_checker", "+8613800138000", "CN"),
        ("wechat_checker", "@hangzhou_export", "CN"),
        ("grab_checker", "+6591234567", "SG"),
    ]

    for service_id, target, country in checks:
        resp = client.post("/v1/verify/service", json={
            "service_id": service_id,
            "target": target,
            "default_country": country,
        })
        assert resp.status_code == 200, f"Failed for {service_id}: {resp.text}"
        data = resp.json()
        assert data["service_id"] == service_id
        assert data["is_registered"] is True
        assert data["cost_credits"] == engine._services_map[service_id].cost_credits
        assert "details" in data
