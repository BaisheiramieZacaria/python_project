from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Optional: Suppress unnecessary browser notifications
options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')

# Start the WebDriver
driver = webdriver.Chrome(options=options)

# Go to the audit page
driver.get("http://10.10.99.18:8002/audit")

# Wait for the page to load
time.sleep(3)  # Use WebDriverWait for production use

try:
    # Look for the "Audits" tab or heading
    audit_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'Audits')]")

    if audit_tab:
        print("✅ Found table name: 'Audits'")
    else:
        print("❌ Table name 'Audits' not found.")

except Exception as e:
    print("⚠️ Error occurred:", e)

# Optional: Close the browser
driver.quit()
