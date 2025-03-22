from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# Function to initialize WebDriver
def initialize_driver():
    browser = webdriver.Chrome()  # Initialize Chrome WebDriver
    browser.maximize_window()
    return browser


# Function to test Facebook login functionality
def test_facebook_login(browser, username, password):
    browser.get("https://www.facebook.com/")  # Open Facebook login page
    time.sleep(2)  # Wait for page to load

    try:
        # Locate Username & Password Fields
        username_field = browser.find_element(By.NAME, "email")
        password_field = browser.find_element(By.NAME, "pass")

        # Enter Username and Password
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit Login Form
        password_field.send_keys(Keys.RETURN)  # Press Enter to log in
        time.sleep(5)  # Wait for login response

    except Exception as e:
        print("An error occurred:", e)


# Test Case Execution
if __name__ == "__main__":
    driver = initialize_driver()

    # Replace with actual credentials (For security, avoid hardcoding credentials)
    fb_username = "09974588180"
    fb_password = "Password"

    test_facebook_login(driver, fb_username, fb_password)

    # Close browser after execution
    time.sleep(50)  # Wait before closing to check login result
    driver.quit()
