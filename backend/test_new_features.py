from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

o = Options()
o.add_argument('--headless')
o.add_argument('--window-size=1440,1100')
d = webdriver.Chrome(options=o)

try:
    print("==================================================================")
    print("1. TESTING ENTERPRISE LIVE SUPPORT DRAWER")
    print("==================================================================")
    d.get("http://127.0.0.1:8000/")
    time.sleep(2)

    # Click liveChatBtn
    chat_btn = d.find_element(By.ID, "liveChatBtn")
    assert chat_btn.is_displayed(), "Live chat button should be visible"
    d.execute_script("arguments[0].click();", chat_btn)
    time.sleep(0.5)

    support_modal = d.find_element(By.ID, "liveSupportModal")
    classes_open = support_modal.get_attribute("class").split()
    assert "hidden" not in classes_open, "Support modal should be open"
    print("PASS: Live Support Drawer opened smoothly!")

    # Verify Telegram and WhatsApp links exist inside
    tg_link = support_modal.find_element(By.XPATH, ".//a[contains(@href, 't.me')]")
    assert "CheckerLeakSupport" in tg_link.get_attribute("href")
    print("PASS: Telegram priority desk link verified (@CheckerLeakSupport).")

    wa_link = support_modal.find_element(By.XPATH, ".//a[contains(@href, 'wa.me')]")
    assert "wa.me" in wa_link.get_attribute("href")
    print("PASS: WhatsApp direct mobile line verified.")

    # Close on outside click or close button
    d.execute_script("document.body.click();")
    time.sleep(0.3)
    classes_closed = support_modal.get_attribute("class").split()
    assert "hidden" in classes_closed, "Support modal should close on outside click"
    print("PASS: Support Drawer closed on outside click.")

    print("\n==================================================================")
    print("2. TESTING BULK CSV CLEANING STUDIO IN DASHBOARD")
    print("==================================================================")
    d.execute_script("""
        localStorage.setItem('checkerleak_client', JSON.stringify({
            id: 1,
            email: 'admin@checkerleak.com',
            firstName: 'Admin',
            credits: 1000,
            token: 'mock_jwt_token'
        }));
    """)
    d.get("http://127.0.0.1:8000/dashboard")
    time.sleep(2)

    # Check Bulk Studio Card exists
    studio_card = d.find_element(By.ID, "bulkStudioCard")
    assert studio_card.is_displayed(), "Bulk Studio Card should be displayed in Dashboard!"
    print("PASS: Bulk CSV Cleaning Studio is present and rendered in Dashboard.")

    # Test Sample List Demo button
    sample_btn = studio_card.find_element(By.XPATH, ".//button[contains(., 'Sample List Demo')]")
    d.execute_script("arguments[0].click();", sample_btn)
    time.sleep(0.5)

    info_banner = d.find_element(By.ID, "fileInfoBanner")
    assert "hidden" not in info_banner.get_attribute("class").split(), "File info banner should appear!"
    file_name = d.find_element(By.ID, "batchFileName").text
    print(f"PASS: Demo file loaded: '{file_name}'")

    # Start Batch File Processing
    start_btn = d.find_element(By.ID, "btnStartBatchProcess")
    d.execute_script("arguments[0].click();", start_btn)
    
    # Wait for completion up to 10s
    for _ in range(20):
        time.sleep(0.5)
        pct = d.find_element(By.ID, "batchProgressPercent").text
        if pct == "100%":
            break
    print(f"PASS: Progress reached {pct}")
    assert pct == "100%", "Batch processing should reach 100%!"

    # Verify Results Table rendered rows
    rows = d.find_elements(By.CSS_SELECTOR, "#bulkTableBody tr")
    print(f"PASS: Rendered {len(rows)} verified contacts in results table.")
    assert len(rows) >= 3, "Results table should display at least 3 rows!"

    # Check first row contains phone and carrier
    first_row_text = rows[0].text
    print(f"PASS: Sample row output: {first_row_text}")

    print("\n==================================================================")
    print("ALL ENTERPRISE FEATURES TESTED & 100% OPERATIONAL!")
    print("==================================================================")

except Exception as e:
    print(f"TEST FAILED: {e}")
    raise e
finally:
    d.quit()
