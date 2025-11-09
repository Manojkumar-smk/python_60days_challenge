from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://the-internet.herokuapp.com/")

# Locate the element using its ID
element = driver.find_element(By.XPATH,'//*[@id="content"]/ul/li[1]/a')
print(element.text)

#wait for 5 seconds to see the result
wait =  WebDriverWait(driver, 5)
wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="content"]/ul/li[1]/a')))

#interact with the element
element.click() 

#screenshot
driver.save_screenshot("screenshot.png")

# Close the browser
driver.quit()

