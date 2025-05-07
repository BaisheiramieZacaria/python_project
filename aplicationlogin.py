from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

driver = webdriver.Chrome()
driver.get("http://10.10.99.18:8002/login")
driver.maximize_window()

wait = WebDriverWait(driver, 20)

try:
    # Log in
    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password = driver.find_element(By.NAME, "password")

    username.clear()
    username.send_keys("Superadmin@gmail.com")

    password.clear()
    password.send_keys("Dost@123")
    password.send_keys(Keys.RETURN)

    wait.until(EC.url_contains("http://10.10.99.18:8002/dashboard"))

    # Navigate to audit form
    driver.get("http://10.10.99.18:8002/audit")

    # Click on add button to open the form
    add_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='fas fa-plus text-white-100']")))
    add_icon.click()

    # Wait for the form or modal to appear
    form_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'audit')]"
)))

    # Normalize and compare the form title
    expected_form_title = "Auditee"
    # Change this to the actual form name you expect
    actual_form_title = re.sub(r'\s+', ' ', form_header.text).strip()

    if actual_form_title == expected_form_title:
        print("✅ Form title correct: 'Auditee'")
    else:
        print(f"❌ Form title mismatch! Expected: '{expected_form_title}'")

    # Wait for form labels to be visible and assert text
    label_checks = [
        ("//label[@for='auditee_audit']", "Audit Title"),
        ("//label[@for='auditee_name']", "Name of Auditee"),
        ("//label[@for='auditee_staff']", "Assigned IAS Staff"),
        ("//label[@for='auditee_remarks']", "Remarks"),

    ]

    for xpath, expected_text in label_checks:
        label = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'audit')]")))
        actual_text = re.sub(r'\s+', ' ', label.text).strip()
        actual_text = re.sub(r'\s*/\s*', ' / ', actual_text)  # Normalize slashes

        if actual_text == expected_text:
            print(f"✅ Label correct: '{actual_text}'")
        else:
            print(f"❌ Label mismatch! Expected: '{expected_text}', Found: '{actual_text}'")

finally:
    driver.quit()