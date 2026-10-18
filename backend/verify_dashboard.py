from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=options)

try:
    # 1. Load page
    driver.get("http://127.0.0.1:8000/dashboard")
    
    # 2. Inject localStorage to simulate login
    driver.execute_script("""
    localStorage.setItem('pulsecheck_client', JSON.stringify({
        firstName: 'Test',
        lastName: 'User',
        email: 'test@example.com',
        credits: 100
    }));
    """)
    driver.refresh()
    time.sleep(1)
    
    # 3. Test Copy API Key
    copy_btn = driver.find_element(By.ID, "copyKeyBtn")
    copy_btn.click()
    time.sleep(0.1) # Wait for UI update
    if "Copied!" in copy_btn.text:
        print("✅ Copy API Key button works!")
    else:
        print("❌ Copy API Key button failed!")

    # 4. Test Refresh Ledger
    refresh_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Refresh Ledger')]")
    refresh_btn.click()
    time.sleep(0.1)
    ledger_body = driver.find_element(By.ID, "portalHistoryBody").text
    if "Syncing blockchain" in ledger_body:
        print("✅ Refresh Ledger button works!")
    else:
        print("❌ Refresh Ledger button failed!")

    # 5. Check JS Errors
    logs = driver.get_log('browser')
    errors = [l['message'] for l in logs if l['level'] == 'SEVERE' and 'favicon.ico' not in l['message']]
    if len(errors) == 0:
        print("✅ No JavaScript errors found in console!")
    else:
        print(f"❌ Found {len(errors)} JS Errors:")
        for e in errors:
            print("  ", e)
            
    # 6. Save proof screenshot
    driver.save_screenshot('dashboard_qa_proof.png')
    print("Screenshot saved to dashboard_qa_proof.png")

except Exception as e:
    print(f"❌ Test script failed: {e}")
finally:
    driver.quit()
