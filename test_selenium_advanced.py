import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pages.login_page import LoginPage

def test_testmu_assignment():
    # 1. Credentials will be read dynamically from your .env file
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    
    if not username or not access_key:
        pytest.fail("Missing credentials! Please update your .env file.")

    grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

    # 2. Basic Grid configuration
    options = ChromeOptions()
    options.browser_version = "latest"
    options.platform_name = "Windows 10"
    
    lt_options = {
        "username": username,
        "access_key": access_key,
        "build": "TestMu Advanced Selenium Exam",
        "name": "Exam Scenario 1",
        "w3c": True
    }
    options.set_capability('LT:Options', lt_options)

    # 3. Spin up the remote browser
    driver = webdriver.Remote(command_executor=grid_url, options=options)

    try:
        # TODO: The assignment URL goes here
        driver.get("https://google.com") 
        
        # Mark test as passed on the cloud dashboard if it hits the end
        driver.execute_script("lambda-status=passed")
    except Exception as e:
        # Mark test as failed on the cloud dashboard if it crashes
        driver.execute_script("lambda-status=failed")
        raise e
    finally:
        driver.quit()
