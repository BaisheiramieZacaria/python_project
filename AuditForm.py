from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# === INIT DRIVER ===
driver = webdriver.Chrome()
driver.get("http://10.10.99.18:8002/login")
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    # === LOGIN ===
    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password = driver.find_element(By.NAME, "password")

    username.clear()
    username.send_keys("Superadmin@gmail.com")

    password.clear()
    password.send_keys("Dost@123")
    password.send_keys(Keys.RETURN)

    wait.until(EC.url_contains("/dashboard"))

    # === NAVIGATE TO AUDIT PAGE ===
    driver.get("http://10.10.99.18:8002/audit")

    # === CLICK 'Annual Compliance Audit' ENTRY ===
    audit_td = wait.until(EC.presence_of_element_located((
        By.XPATH, "//td[normalize-space(text())='Annual Compliance Audit']"
    )))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", audit_td)
    time.sleep(0.5)

    try:
        audit_td.click()
    except Exception:
        driver.execute_script("arguments[0].click();", audit_td)

    time.sleep(2)

    # === CLICK THE PLUS/ADD AUDITEE BUTTON ===
    add_button = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, 'button[data-bs-target="#AuditeeModal"]'
    )))
    try:
        add_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", add_button)

    time.sleep(1)

    # === VERIFY FORM LABELS ===
    label_checks = [
        ("//label[contains(text(), 'Name of Auditee')]", "Name of Auditee"),
        ("//label[contains(text(), 'Assigned IAS Staff')]", "Assigned IAS Staff"),
        ("//label[contains(text(), 'Remarks')]", "Remarks")
    ]

    for xpath, expected_text in label_checks:
        label = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="aue_remarks"]')))

        actual_text = re.sub(r'\s+', ' ', label.text).strip()

        if actual_text == expected_text:
            print(f"✅ Label correct: '{actual_text}'")
        else:
            print(f"❌ Label mismatch! Expected: '{expected_text}', Found: '{actual_text}'")

    # === VERIFY REMARKS INPUT FIELD ===
    remarks_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="aue_remarks"]')))
    remarks_input.send_keys("Sample remarks input.")
    print("✅ Remarks input field is visible and working.")

finally:
    time.sleep(2)
    driver.quit()
