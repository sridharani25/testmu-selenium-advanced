import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

def test_lambdatest_google():
    # 1. Fetch credentials from the configuration
    username = os.getenv("LT_USERNAME", "your_username")
    access_key = os.getenv("LT_ACCESS_KEY", "your_access_key")
    
    grid_url = f"https://{username}:{access_key}@://lambdatest.com"

    # 2. Configure TestMu AI (LambdaTest) capabilities
    options = ChromeOptions()
    options.browser_version = "latest"
    options.platform_name = "Windows 10"
    
    lt_options = {
        "username": username,
        "access_key": access_key,
        "build": "TestMu Advanced Selenium Python Build",
        "name": "Google Title Verification Test",
        "w3c": True,
        "plugin": "python-python"
    }
    options.set_capability('LT:Options', lt_options)

    # 3. Initialize the Remote Web Driver
    driver = webdriver.Remote(command_executor=grid_url, options=options)

    try:
        # 4. Execute the Test Logic
        driver.get("https://google.com")
        assert "Google" in driver.title
        
        # Mark test as passed on the TestMu dashboard
        driver.execute_script("lambda-status=passed")
    except Exception as e:
        # Mark test as failed if an assertion error occurs
        driver.execute_script("lambda-status=failed")
        raise e
    finally:
        # 5. Clean up and close the browser session
        driver.quit()
