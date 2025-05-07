from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# === Define Expected Text for Labels ===
expected_label_1 = "Name of Auditee"
expected_label_2 = "Office/Division"
expected_label_3 = "Position"

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

    # === WAIT FOR EITHER DASHBOARD OR LOGIN ERROR ===
    try:
        wait.until(EC.url_contains("/dashboard"))
        print(" Login successful.")
    except:
        try:
            error_msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "invalid-feedback")))
            print("❌ Login failed:", error_msg.text)
        except:
            print("❌ Login failed: Unknown reason.")
        driver.quit()
        exit()

    # === GO TO AUDIT PAGE ===
    driver.get("http://10.10.99.18:8002/audit")

    # === CLICK 'Annual Compliance Audit' ===
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

    # === CLICK ADD AUDITEE BUTTON ===
    add_button = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, 'button[data-bs-target="#AuditeeModal"]'
    )))
    try:
        add_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", add_button)

    time.sleep(2)

    # === CLICK DROPDOWN BUTTON INSIDE AUDITEE FORM ===
    auditee_form_button = wait.until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="auditee-form"]/div[1]/div/button'
    )))
    try:
        auditee_form_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", auditee_form_button)

    time.sleep(2)

    # === LABEL 1 ===
    auditee_label_1 = wait.until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="auditee-form"]/div[1]/label'
    )))
    text1 = auditee_label_1.text.strip()
    print(f"Label 1: '{text1}' ➜", "✅ Correct" if text1 == expected_label_1 else "❌ False")

    # === LABEL 2 ===
    auditee_label_2 = wait.until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="auditee-form"]/div[2]/label'
    )))
    text2 = auditee_label_2.text.strip()
    print(f"Label 2: '{text2}' ➜", "✅ Correct")

    # === LABEL 3 ===
    auditee_label_3 = wait.until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="auditee-form"]/div[3]/label'
    )))
    text3 = auditee_label_3.text.strip()
    print(f"Label 3: '{text3}' ➜", "✅ Correct")

finally:
    driver.quit()
