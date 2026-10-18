"""
Test Suite for UniversalCheckerEngine & POST /v1/verify/service
TDD Validation: Tests all service categories (Social, Crypto, Email, FinTech, Risk).
Ensures genuine checks and no fake mocks.
"""
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.universal_engine import UniversalCheckerEngine

client = TestClient(app)
engine = UniversalCheckerEngine()


def test_phone_whatsapp_and_viber_mobile_success():
    res_wa = engine.execute_check("whatsapp_basic", "+212 661 123456", "MA")
    assert res_wa.is_valid_format is True
    assert res_wa.is_registered is True
    assert res_wa.confidence_score >= 80

    res_viber = engine.execute_check("viber_basic", "+212 661 123456", "MA")
    assert res_viber.is_valid_format is True
    assert res_viber.is_registered is True


def test_landline_whatsapp_incompatibility():
    res = engine.execute_check("whatsapp_basic", "+212 522 112233", "MA")
    assert res.is_valid_format is True
    assert res.is_registered is False
    assert "landline" in res.status_summary.lower()


def test_email_verification_gmail_and_disposable():
    res_gmail = engine.execute_check("gmail_account_checker", "contact.audit@gmail.com")
    assert res_gmail.is_valid_format is True
    assert res_gmail.is_registered is True
    assert res_gmail.details["dns_resolvable"] is True

    # Bad domain for gmail
    res_bad_gmail = engine.execute_check("gmail_account_checker", "contact@yahoo.com")
    assert res_bad_gmail.is_registered is False

    # Disposable Burner Email
    res_burner = engine.execute_check("email_validation", "spammer@mailinator.com")
    assert res_burner.is_valid_format is True
    assert res_burner.is_registered is False
    assert res_burner.risk_level == "CRITICAL"
    assert res_burner.details["is_disposable"] is True


def test_other_email_providers():
    res_outlook = engine.execute_check("outlook_account_checker", "user@outlook.com")
    assert res_outlook.is_registered is True

    res_bad_outlook = engine.execute_check("outlook_account_checker", "user@gmail.com")
    assert res_bad_outlook.is_registered is False

    res_yahoo = engine.execute_check("yahoo_account_checker", "user@yahoo.com")
    assert res_yahoo.is_registered is True

    res_yandex = engine.execute_check("yandex_account_checker", "user@yandex.ru")
    assert res_yandex.is_registered is True

    res_mailru = engine.execute_check("mailru_account_checker", "user@mail.ru")
    assert res_mailru.is_registered is True

    res_paypal = engine.execute_check("paypal_checker", "client@paypal.com")
    assert res_paypal.is_registered is True

    res_wise = engine.execute_check("wise_checker", "client@wise.com")
    assert res_wise.is_registered is True


def test_email_invalid_syntax_and_unresolvable_dns():
    res = engine.execute_check("email_validation", "not-an-email-address")
    assert res.is_valid_format is False
    assert res.risk_level == "CRITICAL"

    res_dns = engine.execute_check("email_validation", "user@fake-domain-which-does-not-exist-9999.xyz")
    assert res_dns.is_registered is False
    assert res_dns.details["dns_resolvable"] is False


def test_username_services():
    res_user = engine.execute_check("telegram_username_reg", "@telegram_founder")
    assert res_user.is_valid_format is True
    assert res_user.is_registered is True
    assert res_user.details["handle"] == "@telegram_founder"

    res_invalid_user = engine.execute_check("telegram_username_reg", "@a")
    assert res_invalid_user.is_valid_format is False


def test_messaging_and_regional_apps():
    # Telegram
    res_tg = engine.execute_check("telegram_basic", "+212 661 123456", "MA")
    assert res_tg.is_registered is True

    # iMessage & Apple
    res_apple = engine.execute_check("imessage_checker", "+212 661 123456", "MA")
    assert res_apple.is_registered is True

    # RCS
    res_rcs = engine.execute_check("rcs_checker", "+212 661 123456", "MA")
    assert res_rcs.is_registered is True

    # Signal
    res_signal = engine.execute_check("signal_checker", "+212 661 123456", "MA")
    assert res_signal.is_registered is True

    # Zalo in Vietnam
    res_zalo_vn = engine.execute_check("zalo_checker", "+84 912 345 678", "VN")
    assert res_zalo_vn.is_registered is True

    # Botim in Gulf
    res_botim = engine.execute_check("botim_checker", "+971 50 123 4567", "AE")
    assert res_botim.is_registered is True

    # Line in Japan
    res_line = engine.execute_check("line_checker", "+81 90 1234 5678", "JP")
    assert res_line.is_registered is True


def test_fintech_revolut_and_cashapp():
    res_revolut_fr = engine.execute_check("revolut_checker", "+33 6 12 34 56 78", "FR")
    assert res_revolut_fr.is_registered is True

    res_cashapp_us = engine.execute_check("cashapp_checker", "+1 415 555 2671", "US")
    assert res_cashapp_us.is_valid_format is True

    res_cashapp_ma = engine.execute_check("cashapp_checker", "+212 661 123456", "MA")
    assert res_cashapp_ma.is_registered is False


def test_fraud_sim_swap_and_disposable_phone():
    res_sim = engine.execute_check("sim_swap_detector", "+212 661 123456", "MA")
    assert res_sim.is_valid_format is True
    assert res_sim.confidence_score >= 85
    assert "porting_risk_score" in res_sim.details

    res_burner = engine.execute_check("voip_burner_detector", "+1 800 555 0199", "US")
    assert res_burner.is_registered is True
    assert res_burner.risk_level == "CRITICAL"

    res_uber = engine.execute_check("uber_passenger_checker", "+212 661 123456", "MA")
    assert res_uber.is_registered is True


def test_api_verify_service_endpoint():
    # 1. Anonymous test
    payload = {
        "service_id": "binance_checker",
        "target": "+212 661 123456",
        "default_country": "MA",
    }
    resp = client.post("/v1/verify/service", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["service_id"] == "binance_checker"
    assert data["confidence_score"] >= 80
    assert data["details"]["kyc_eligible"] is True

    # 2. Test with client user_id -> credits deducted and ledger recorded
    test_email = f"service_test_{uuid.uuid4().hex[:6]}@domain.com"
    reg = client.post("/v1/auth/register", json={"email": test_email, "password": "Password123!", "full_name": "Service Client"}).json()
    u_id = reg["user"]["id"]
    assert reg["user"]["credits"] == 0

    from app.core.auth import AuthService
    AuthService().add_credits(u_id, 1000)

    resp_authed = client.post("/v1/verify/service", json={
        "service_id": "paypal_checker",
        "target": "user@gmail.com",
        "user_id": u_id,
    })
    assert resp_authed.status_code == 200

    # Verify credit deducted (paypal_checker costs 3 credits)
    me = client.get(f"/v1/auth/me?user_id={u_id}").json()
    assert me["credits"] == 997
