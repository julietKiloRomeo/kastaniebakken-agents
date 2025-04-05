from selenium import webdriver
import os

url = f"""http://{os.environ["SELENIUM_HOST"]}:{os.environ["SELENIUM_PORT"]}"""
driver = webdriver.Remote(
    command_executor=url,
    options = webdriver.ChromeOptions(),    
)

driver.get("https://www.google.com")
print(driver.title)