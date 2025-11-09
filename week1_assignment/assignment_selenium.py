from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialize the Chrome driver (make sure chromedriver is in PATH or specify path)
driver = webdriver.Chrome()

try:
    # Navigate to the main page
    driver.get("https://the-internet.herokuapp.com/")
    
    # Wait for the page to load and find the link using the provided XPath
    wait = WebDriverWait(driver, 10)
    link = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/ul/li[27]/a")))
    link.click()
    
    # Wait for the input field to be present and clickable
    input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/div/div/input")))
    input_field.click()  # Click on the input as specified
    
    # Fill in a number (e.g., 42)
    input_field.clear()  # Clear any existing value
    input_field.send_keys("42")  # Fill number here
    
    # Take screenshot after entering the number
    driver.save_screenshot("after_entering_number.png")
    
    # Optional: Print the value entered
    print("Number entered:", input_field.get_attribute("value"))
    
except TimeoutException:
    print("Timeout waiting for page element to load")
    
finally:
    # Close the browser
    driver.quit()