from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=options)

driver.get("http://127.0.0.1:8000/dashboard")
time.sleep(3) # wait for render

# Check console logs for errors
logs = driver.get_log('browser')
for l in logs:
    if l['level'] == 'SEVERE':
        print('JS ERROR:', l['message'])

# Take screenshot
driver.save_screenshot('dashboard_screenshot.png')
print("Screenshot saved to dashboard_screenshot.png")

# Check if the grid actually rendered anything
rendered_items = driver.execute_script("return document.querySelectorAll('#servicesDirectoryContainer .group').length;")
print("Number of rendered service cards:", rendered_items)

driver.quit()
