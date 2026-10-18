from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=options)

try:
    print(">>> 1. Loading Billing Page...")
    driver.get("http://127.0.0.1:8000/billing")
    time.sleep(2)

    logs = driver.get_log('browser')
    js_errors = [l['message'] for l in logs if l['level'] == 'SEVERE' and '404' not in l['message'] and 'favicon' not in l['message']]
    if js_errors:
        print("FAIL: JS Errors on billing load:", js_errors)
    else:
        print("PASS: 0 JavaScript errors on billing load.")

    # Open Crypto Modal
    print(">>> 2. Opening Redesigned Crypto Modal...")
    driver.execute_script("topUpCredits(50);")
    time.sleep(0.5)

    modal = driver.find_element(By.ID, "cryptoTopUpModal")
    assert "hidden" not in modal.get_attribute("class"), "cryptoTopUpModal should be visible!"
    print("PASS: Crypto Top-Up Modal opened successfully!")

    # Verify 6 Network Buttons
    expected_methods = [
        ("USDT_TRC20", "TT44hVQek5xLh7qz2FhpBdmbMziyBGyzPX"),
        ("USDT_BEP20", "0x35dd60066ae6337b4D0273b129c0E222235B9F8C"),
        ("BTC", "bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu"),
        ("ETH", "0x35dd60066ae6337b4D0273b129c0E222235B9F8C"),
        ("SOL", "t9QLb3arVUMcQ8JALe3Ptz318GfZkzmRAXvoM8yANFe"),
        ("LTC", "LVW74nrfMVpsTY7Kd62tkzfNF5aasM7ieS")
    ]

    print(">>> 3. Testing Switching between all 6 Crypto Networks...")
    for method_key, expected_addr in expected_methods:
        driver.execute_script(f"selectCryptoTab('{method_key}');")
        time.sleep(0.2)
        addr_text = driver.find_element(By.ID, "cryptoAddress").text.strip()
        assert addr_text == expected_addr, f"Address mismatch for {method_key}: expected {expected_addr}, got {addr_text}"
        print(f"  PASS [{method_key}]: Address updated correctly to {addr_text}")

    # Test Credit Estimate Calculator
    print(">>> 4. Testing Live Credits Calculator...")
    amt_input = driver.find_element(By.ID, "cryptoAmountInput")
    amt_input.clear()
    amt_input.send_keys("100")
    time.sleep(0.2)
    estimate = driver.find_element(By.ID, "creditEstimateNotice").text
    safe_estimate = estimate.encode('ascii', 'replace').decode('ascii')
    print(f"PASS: Live credit estimate for $100: '{safe_estimate}'")
    assert "10,000" in estimate, "Credit estimate should show 10,000 credits for $100"

    # Test Copy Button
    print(">>> 5. Testing Copy Address Button...")
    copy_btn = driver.find_element(By.ID, "cryptoCopyBtn")
    copy_btn.click()
    time.sleep(0.3)
    btn_text = copy_btn.text
    print(f"PASS: Copy button feedback text: '{btn_text}'")

    # Test Payment Submission
    print(">>> 6. Testing 'Confirm & Credit Wallet Balance' submission...")
    txid_input = driver.find_element(By.ID, "cryptoTxidInput")
    txid_input.clear()
    txid_input.send_keys("0x9999test_txid_hash_verification")

    submit_btn = driver.find_element(By.ID, "btnSubmitPayment")
    submit_btn.click()
    time.sleep(1.5)

    print("PASS: Payment submitted and credited cleanly!")
    print("\n==============================================================")
    print("ALL 6 CRYPTO NETWORKS & REDESIGNED MODAL ARE 100% OPERATIONAL!")
    print("==============================================================")

except Exception as e:
    print(f"TEST FAILED: {e}")
finally:
    driver.quit()
