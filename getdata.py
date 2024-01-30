from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
import time
import re
def get_token_price():
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.taptools.io/?Tokens=Recently+Added")
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[8]/div[1]")))
        tagname = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[1]")))
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.save_screenshot("screenshot.png")
        price = element.text
        tagname=tagname.text
        price = re.sub("[^0-9.]", "", price)
        price = float(re.sub("[^0-9.]", "", price))
        return price, tagname
    except:
        driver.refresh()
        return 0,0