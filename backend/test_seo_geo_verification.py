import urllib.request
import xml.etree.ElementTree as ET
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_index_hreflang():
    print("\n--- 1. Testing index.html hreflang tags ---")
    url = f"{BASE_URL}/"
    req = urllib.request.urlopen(url)
    assert req.status == 200, f"Expected 200, got {req.status}"
    html = req.read().decode('utf-8')
    expected_langs = ['en', 'es', 'pt', 'id', 'de', 'tr', 'ru', 'zh-CN', 'x-default']
    for lang in expected_langs:
        tag = f'hreflang="{lang}"'
        assert tag in html, f"Missing hreflang: {tag}"
        print(f"  [OK] Found {tag}")
    print("[PASS] index.html hreflang verified.")

def test_robots_txt():
    print("\n--- 2. Testing robots.txt AI bots ---")
    url = f"{BASE_URL}/robots.txt"
    req = urllib.request.urlopen(url)
    assert req.status == 200, f"Expected 200, got {req.status}"
    content = req.read().decode('utf-8')
    expected_bots = [
        'GPTBot', 'OAI-SearchBot', 'ClaudeBot', 'Claude-Web', 
        'PerplexityBot', 'Applebot-Extended', 'Google-Extended', 
        'CCBot', 'Meta-ExternalAgent', 'Amazonbot', 'cohere-ai'
    ]
    for bot in expected_bots:
        assert f"User-agent: {bot}" in content, f"Missing bot in robots.txt: {bot}"
        print(f"  [OK] Found crawler rule for: {bot}")
    assert "Sitemap: https://checkerleak.com/sitemap.xml" in content
    print("[PASS] robots.txt AI bots verified.")

def test_sitemap_xml():
    print("\n--- 3. Testing sitemap.xml ---")
    url = f"{BASE_URL}/sitemap.xml"
    req = urllib.request.urlopen(url)
    assert req.status == 200, f"Expected 200, got {req.status}"
    raw_xml = req.read().decode('utf-8')
    
    # Assert NO hash anchors in sitemap
    assert "#" not in raw_xml, "Error: Found hash fragment '#' in sitemap.xml!"
    
    # Parse XML
    root = ET.fromstring(raw_xml)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [loc.text for loc in root.findall('ns:url/ns:loc', namespace)]
    print(f"  [OK] Total parsed URLs in sitemap: {len(urls)}")
    
    product_urls = [u for u in urls if "/products/" in u]
    cat_urls = [u for u in urls if "/categories/" in u]
    geo_urls = [u for u in urls if "geo=" in u]
    
    print(f"  [OK] Categories in sitemap: {len(cat_urls)} (Expected: 6)")
    print(f"  [OK] Products in sitemap: {len(product_urls)} (Expected: 102)")
    print(f"  [OK] Geo hubs in sitemap: {len(geo_urls)}")
    
    assert len(cat_urls) == 6, f"Expected 6 categories, got {len(cat_urls)}"
    assert len(product_urls) == 102, f"Expected 102 products, got {len(product_urls)}"
    print("[PASS] sitemap.xml verified with zero hash fragments and 100% engine coverage.")

def test_llms_txt():
    print("\n--- 4. Testing llms.txt & llms-full.txt ---")
    for endpoint in ["/llms.txt", "/llms-full.txt"]:
        url = f"{BASE_URL}{endpoint}"
        req = urllib.request.urlopen(url)
        assert req.status == 200, f"Expected 200 for {endpoint}, got {req.status}"
        text = req.read().decode('utf-8')
        assert "CheckerLeak.com" in text
        assert "102" in text
        print(f"  [OK] {endpoint} verified ({len(text)} bytes).")
    print("[PASS] LLM GEO endpoints verified.")

def test_product_and_category_pages():
    print("\n--- 5. Testing programmatic product & category canonical URLs ---")
    
    # Test product canonical
    test_slug = "binance-checker"
    url = f"{BASE_URL}/products/{test_slug}"
    req = urllib.request.urlopen(url)
    assert req.status == 200, f"Expected 200, got {req.status}"
    html = req.read().decode('utf-8')
    assert '<link rel="canonical" href="https://checkerleak.com/products/binance-checker">' in html, "Canonical mismatch!"
    assert '"url": "https://checkerleak.com/products/binance-checker"' in html, "Schema URL mismatch!"
    print(f"  [OK] /products/{test_slug} rendered exact canonical tag & Schema.org URL.")
    
    # Test category canonical
    cat_slug = "crypto-exchange"
    url = f"{BASE_URL}/categories/{cat_slug}"
    req = urllib.request.urlopen(url)
    assert req.status == 200, f"Expected 200, got {req.status}"
    html = req.read().decode('utf-8')
    assert '<link rel="canonical" href="https://checkerleak.com/categories/crypto-exchange">' in html
    print(f"  [OK] /categories/{cat_slug} rendered exact canonical tag.")
    
    print("[PASS] Programmatic SEO routes and canonical URLs verified.")

if __name__ == "__main__":
    try:
        test_index_hreflang()
        test_robots_txt()
        test_sitemap_xml()
        test_llms_txt()
        test_product_and_category_pages()
        print("\n=======================================================")
        print(">>> ALL 5 SEO & GEO VERIFICATIONS PASSED PERFECTLY! <<<")
        print("=======================================================\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FAIL] Verification error: {e}")
        sys.exit(1)
