"""
Automated Test Suite for CheckerLeak Blog & Content Engine
Verifies that:
1. /blog returns HTTP 200 with all 4 technical articles listed.
2. Each article route returns HTTP 200, valid Schema.org JSON-LD (BlogPosting), BreadcrumbList, and canonical tags.
3. Sitemap contains all blog URLs.
"""
import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_blog():
    print("--- 1. Testing Blog Index ---")
    req = urllib.request.urlopen(f"{BASE_URL}/blog")
    assert req.status == 200, f"Expected 200, got {req.status}"
    html = req.read().decode('utf-8')
    assert "Telecom Intelligence, HLR Signaling" in html
    assert "how-to-check-if-phone-number-is-active-without-calling" in html
    assert "voip-vs-mobile-number-how-to-detect-virtual-burners" in html
    assert "how-to-check-apple-imessage-blue-bubble-status-api" in html
    assert "phone-number-osint-investigation-footprint-guide" in html
    print("  [OK] /blog renders index with 4 deep technical guides.")

    articles = [
        "how-to-check-if-phone-number-is-active-without-calling",
        "voip-vs-mobile-number-how-to-detect-virtual-burners",
        "how-to-check-apple-imessage-blue-bubble-status-api",
        "phone-number-osint-investigation-footprint-guide"
    ]

    print("\n--- 2. Testing Individual Blog Articles ---")
    for slug in articles:
        url = f"{BASE_URL}/blog/{slug}"
        req = urllib.request.urlopen(url)
        assert req.status == 200, f"Expected 200 for {url}, got {req.status}"
        body = req.read().decode('utf-8')
        assert f'<link rel="canonical" href="https://checkerleak.com/blog/{slug}">' in body
        assert '"@type": "BlogPosting"' in body
        assert '"@type": "BreadcrumbList"' in body
        assert "CheckerLeak.com" in body
        print(f"  [OK] /blog/{slug} verified with canonical URL & Schema JSON-LD.")

    print("\n--- 3. Testing Sitemap Blog Inclusion ---")
    s_req = urllib.request.urlopen(f"{BASE_URL}/sitemap.xml")
    s_xml = s_req.read().decode('utf-8')
    assert "<loc>https://checkerleak.com/blog</loc>" in s_xml
    for slug in articles:
        assert f"<loc>https://checkerleak.com/blog/{slug}</loc>" in s_xml
    print("  [OK] sitemap.xml contains all blog URLs.")

if __name__ == "__main__":
    try:
        test_blog()
        print("\n=======================================================")
        print(">>> ALL BLOG & CONTENT ENGINE TESTS PASSED (100%)! <<<")
        print("=======================================================\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FAIL] Blog test error: {e}")
        sys.exit(1)
