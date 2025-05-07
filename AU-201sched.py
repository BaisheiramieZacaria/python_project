from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# === START DRIVER ===
driver = webdriver.Chrome()
driver.get("http://10.10.99.18:8002/login")
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    # === LOGIN ===
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("Superadmin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("Dost@123" + Keys.RETURN)

    wait.until(EC.url_contains("/dashboard"))

    # === GO TO AUDIT PAGE ===
    driver.get("http://10.10.99.18:8002/audit")
    time.sleep(2)


    audit_td = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="auditees-tab"]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", audit_td)
    time.sleep(0.5)
    try:
        audit_td.click()
    except:
        driver.execute_script("arguments[0].click();", audit_td)

    time.sleep(2)

    # === CLICK 'ADD AUDITEE' BUTTON ===
    add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '//*[@id="auditees-tab"]')))
    try:
        add_button.click()
    except:
        driver.execute_script("arguments[0].click();", add_button)

    time.sleep(1)


    print("✅ Auditee form submitted successfully!")

finally:
    time.sleep(3)
    driver.quit()
