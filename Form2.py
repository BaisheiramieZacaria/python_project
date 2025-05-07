from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

    # === PUNTA SA AUDIT PAGE ===
    driver.get("http://10.10.99.18:8002/audit")

    # === HANAPIN ANG <td> NA MAY TEXT NA 'Annual Compliance Audit' AT I-CLICK ===
    audit_td = wait.until(EC.presence_of_element_located((
        By.XPATH, "//td[normalize-space(text())='Annual Compliance Audit']"
    )))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", audit_td)
    time.sleep(0.5)

    try:
        audit_td.click()
    except Exception:
        driver.execute_script("arguments[0].click();", audit_td)

    time.sleep(2)  # Optional to see the result

    # === CLICK THE ADD AUDITEE BUTTON ===
    add_button = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, 'button[data-bs-target="#AuditeeModal"]'
    )))
    try:
        add_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", add_button)

    time.sleep(2)  # Optional to see modal open

finally:
    driver.quit()