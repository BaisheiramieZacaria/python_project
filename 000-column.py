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

    # === GO TO AUDIT PAGE ===
    driver.get("http://10.10.99.18:8002/audit")
    time.sleep(2)

    # === WAIT FOR TABLE HEADERS ===
    header_xpath = '//*[@id="DataTables_Table_1_wrapper"]/div[2]/div/div/div[1]/div/table/thead/tr/th'
    header_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, header_xpath)))

    actual_headers = []
    for idx, th in enumerate(header_elements, start=1):
        text = th.text.strip()
        if not text:
            # Try getting specific spans inside header cells if no direct text found
            try:
                text = th.find_element(By.XPATH, f".//span[1]").text.strip()
            except:
                text = ""

        cleaned_text = re.sub(r'\s+', ' ', text)
        actual_headers.append(cleaned_text)

    expected_headers = [
        "No.",
        "Title",
        "Auditee",
        "Type of Audit",
        "Agency Program/Project/System/Process",
        "Duration",
        "STATUS",
        "Description/Remarks"
    ]

    print("\n🧾 Checking column headers...\n")
    for expected in expected_headers:
        if expected in actual_headers:
            print(f"✅ Found column: {expected}")
        else:
            print(f"❌ Missing column: {expected}")

finally:
    time.sleep(2)

