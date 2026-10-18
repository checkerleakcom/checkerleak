"""
Test suite for Services Catalog - TDD
Validates that all 80+ checkers and exclusive engines are indexed, categorized, and queryable.
"""
from fastapi.testclient import TestClient
from app.main import app
from app.core.services_catalog import get_all_services, get_services_by_category, ServiceCategory

client = TestClient(app)


def test_services_catalog_contains_all_services():
    services = get_all_services()
    assert len(services) >= 80, f"Expected at least 80 services, found {len(services)}"

    service_ids = {s.id for s in services}
    # Check key services from screenshots
    assert "telegram_basic" in service_ids
    assert "telegram_days" in service_ids
    assert "telegram_age_gender" in service_ids
    assert "whatsapp_bulk" in service_ids
    assert "whatsapp_advanced" in service_ids
    assert "whatsapp_days" in service_ids
    assert "whatsapp_age_gender" in service_ids
    assert "viber_basic" in service_ids
    assert "viber_days" in service_ids
    assert "viber_avatar_demographics" in service_ids
    assert "imessage_checker" in service_ids
    assert "rcs_checker" in service_ids
    assert "carrier_detection" in service_ids
    assert "apple_checker" in service_ids
    assert "facebook_checker" in service_ids
    assert "amazon_checker" in service_ids
    assert "instagram_checker" in service_ids
    assert "netflix_number_checker" in service_ids
    assert "botim_checker" in service_ids
    assert "linkedin_number_checker" in service_ids
    assert "zalo_checker" in service_ids
    assert "vkontakte_checker" in service_ids
    assert "signal_checker" in service_ids
    assert "twitter_checker" in service_ids
    assert "tiktok_checker" in service_ids
    assert "microsoft_checker" in service_ids
    assert "snapchat_checker" in service_ids
    assert "kucoin_checker" in service_ids
    assert "binance_checker" in service_ids
    assert "okx_checker" in service_ids
    assert "gmail_account_checker" in service_ids
    assert "outlook_account_checker" in service_ids
    assert "yahoo_account_checker" in service_ids

    # Check our exclusive additions
    assert "paypal_checker" in service_ids
    assert "revolut_checker" in service_ids
    assert "wise_checker" in service_ids
    assert "cashapp_checker" in service_ids
    assert "sim_swap_detector" in service_ids
    assert "voip_burner_detector" in service_ids


def test_services_api_endpoint():
    res = client.get("/v1/services")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 80

    # Filter by category
    crypto_res = client.get("/v1/services?category=CRYPTO_EXCHANGE")
    assert crypto_res.status_code == 200
    crypto_data = crypto_res.json()
    assert len(crypto_data) >= 8
    for item in crypto_data:
        assert item["category"] == "CRYPTO_EXCHANGE"
