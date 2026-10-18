"""
Unit and integration tests for Geo & Telecom Intelligence, Visitor Geolocation,
and SEO/GEO Crawler Endpoints (robots.txt, sitemap.xml, llms.txt).
"""
from fastapi.testclient import TestClient
from app.main import app
from app.core.geo_intelligence import GeoIntelligenceService

client = TestClient(app)
geo_service = GeoIntelligenceService()


def test_geo_service_catalog():
    countries = geo_service.get_supported_countries()
    assert len(countries) >= 8
    iso_codes = [c["iso"] for c in countries]
    assert "MA" in iso_codes
    assert "US" in iso_codes
    assert "FR" in iso_codes
    assert "AE" in iso_codes

    # Test detailed profile lookup
    ma_profile = geo_service.get_country_profile("MA")
    assert ma_profile is not None
    assert ma_profile.name == "Morocco"
    assert ma_profile.dial_code == "+212"
    assert len(ma_profile.carriers) >= 3
    carrier_names = [c.name for c in ma_profile.carriers]
    assert any("Maroc Telecom" in name for name in carrier_names)


def test_geo_visitor_detection():
    # 1. Cloudflare header
    profile_us = geo_service.detect_visitor_geo({"cf-ipcountry": "US"})
    assert profile_us.iso == "US"

    # 2. X-Country-Code header
    profile_fr = geo_service.detect_visitor_geo({"x-country-code": "FR"})
    assert profile_fr.iso == "FR"

    # 3. Accept-Language header
    profile_es = geo_service.detect_visitor_geo({"accept-language": "es-ES,es;q=0.9"})
    assert profile_es.iso == "ES"

    # 4. Fallback
    profile_fallback = geo_service.detect_visitor_geo({})
    assert profile_fallback.iso == "MA"


def test_geo_router_endpoints():
    # Detect endpoint
    res = client.get("/v1/geo/detect", headers={"cf-ipcountry": "FR"})
    assert res.status_code == 200
    data = res.json()
    assert data["iso"] == "FR"
    assert data["dial_code"] == "+33"

    # List countries endpoint
    res = client.get("/v1/geo/countries")
    assert res.status_code == 200
    countries = res.json()
    assert len(countries) >= 8

    # Specific country endpoint
    res = client.get("/v1/geo/country/AE")
    assert res.status_code == 200
    ae_data = res.json()
    assert ae_data["name"] == "United Arab Emirates"
    assert ae_data["dial_code"] == "+971"

    # 404 for unknown ISO
    res = client.get("/v1/geo/country/ZZ")
    assert res.status_code == 404


def test_seo_and_geo_crawler_endpoints():
    # 1. robots.txt
    res = client.get("/robots.txt")
    assert res.status_code == 200
    assert "User-agent: *" in res.text
    assert "Sitemap: https://checkerleak.com/sitemap.xml" in res.text

    # 2. sitemap.xml
    res = client.get("/sitemap.xml")
    assert res.status_code == 200
    assert "<loc>https://checkerleak.com/</loc>" in res.text
    assert "<loc>https://checkerleak.com/docs</loc>" in res.text

    # 3. llms.txt (Generative Engine Optimization)
    res = client.get("/llms.txt")
    assert res.status_code == 200
    assert "CheckerLeak.com" in res.text
    assert "Core Capabilities" in res.text

    # 4. llms-full.txt
    res = client.get("/llms-full.txt")
    assert res.status_code == 200
    assert "Complete Technical Reference" in res.text
