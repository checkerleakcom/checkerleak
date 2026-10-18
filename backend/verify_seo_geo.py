"""
Verification script for SEO & GEO Infrastructure on CheckerLeak.com
"""
import urllib.request
import json

def test_seo_and_geo():
    print("--- 1. Testing Homepage HTML for SEO & Structured Data ---")
    res = urllib.request.urlopen("http://127.0.0.1:8000/")
    html = res.read().decode("utf-8")
    
    assert '<meta name="description"' in html, "Missing meta description"
    assert '<link rel="canonical" href="https://checkerleak.com/">' in html, "Missing canonical link"
    assert 'property="og:title"' in html, "Missing OpenGraph title"
    assert 'name="twitter:card"' in html, "Missing Twitter Card"
    assert '"@type": "SoftwareApplication"' in html, "Missing SoftwareApplication JSON-LD"
    assert '"@type": "FAQPage"' in html, "Missing FAQPage JSON-LD"
    assert 'id="geoTargetSection"' in html, "Missing geoTargetSection in HTML"
    assert 'id="faqSection"' in html, "Missing faqSection in HTML"
    print("Homepage SEO, OpenGraph, JSON-LD, GeoHub & FAQ: VERIFIED OK")

    print("\n--- 2. Testing Crawler & AI Engine Directives ---")
    # robots.txt
    res = urllib.request.urlopen("http://127.0.0.1:8000/robots.txt")
    assert res.status == 200
    robots_txt = res.read().decode("utf-8")
    assert "User-agent: *" in robots_txt
    assert "Sitemap: https://checkerleak.com/sitemap.xml" in robots_txt
    print("robots.txt: VERIFIED OK")

    # sitemap.xml
    res = urllib.request.urlopen("http://127.0.0.1:8000/sitemap.xml")
    assert res.status == 200
    sitemap_xml = res.read().decode("utf-8")
    assert "<loc>https://checkerleak.com/</loc>" in sitemap_xml
    assert "<loc>https://checkerleak.com/docs</loc>" in sitemap_xml
    assert "<loc>https://checkerleak.com/llms.txt</loc>" in sitemap_xml
    print("sitemap.xml: VERIFIED OK")

    # llms.txt (Generative Engine Optimization)
    res = urllib.request.urlopen("http://127.0.0.1:8000/llms.txt")
    assert res.status == 200
    llms_txt = res.read().decode("utf-8")
    assert "CheckerLeak.com" in llms_txt
    assert "Core Capabilities" in llms_txt
    print("llms.txt (Generative Engine Optimization): VERIFIED OK")

    # llms-full.txt
    res = urllib.request.urlopen("http://127.0.0.1:8000/llms-full.txt")
    assert res.status == 200
    llms_full = res.read().decode("utf-8")
    assert "Complete Technical Reference" in llms_full
    print("llms-full.txt (Full AI Documentation): VERIFIED OK")

    print("\n--- 3. Testing Geo & Telecom Intelligence API ---")
    # /v1/geo/detect
    req = urllib.request.Request("http://127.0.0.1:8000/v1/geo/detect", headers={"cf-ipcountry": "MA"})
    res = urllib.request.urlopen(req)
    geo_data = json.loads(res.read().decode("utf-8"))
    assert geo_data["iso"] == "MA"
    assert geo_data["dial_code"] == "+212"
    assert len(geo_data["carriers"]) >= 3
    print(f"Geo Detect (Morocco): {geo_data['name']} ({geo_data['dial_code']}) with {len(geo_data['carriers'])} MNOs: VERIFIED OK")

    # /v1/geo/countries
    res = urllib.request.urlopen("http://127.0.0.1:8000/v1/geo/countries")
    countries = json.loads(res.read().decode("utf-8"))
    assert len(countries) >= 8
    print(f"Geo Country Catalog: {len(countries)} primary hubs indexed: VERIFIED OK")

    # /v1/geo/country/US
    res = urllib.request.urlopen("http://127.0.0.1:8000/v1/geo/country/US")
    us_data = json.loads(res.read().decode("utf-8"))
    assert us_data["iso"] == "US"
    assert us_data["dial_code"] == "+1"
    assert us_data["imessage_share_pct"] > 50
    print(f"Geo Profile (US): Blue-bubble dominance {us_data['imessage_share_pct']}%: VERIFIED OK")

    print("\nSUCCESS: ALL SEO & GEO COMPONENTS OPERATING AT 100% HEALTH!")

if __name__ == "__main__":
    test_seo_and_geo()
