import os
import sys
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key.strip()] = value.strip()

from pages.main_page import MainPage
from pages.agentic_page import AgenticCloudPage
from pages.blog_page import BlogPage

CONFIGURATIONS = [
    {"browser": "Chrome", "version": "128.0", "platform": "Windows 10", "build": "Scenario 1 - Chrome"},
    {"browser": "MicrosoftEdge", "version": "127.0", "platform": "macOS Ventura", "build": "Scenario 2 - Edge"}
]

@pytest.mark.parametrize("config", CONFIGURATIONS)
def test_testmu_advanced_assignment(config):
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    
    if not username or not access_key:
        pytest.fail("Credentials missing from .env file!")

    grid_url = "https://hub.lambdatest.com/wd/hub"

    if config["browser"] == "Chrome":
        options = ChromeOptions()
    else:
        options = EdgeOptions()

    options.browser_version = config["version"]
    options.platform_name = config["platform"]

    lt_options = {
        "user": username,
        "accessKey": access_key,
        "build": "TestMu Advanced Certification Suite",
        "name": f"Running on {config['browser']}",
        "w3c": True,
        "network": True,
        "video": True,
        "visual": True,
        "console": True
    }
    options.set_capability('LT:Options', lt_options)

    driver = webdriver.Remote(command_executor=grid_url, options=options)
    driver.set_page_load_timeout(20)

    try:
        driver.get("https://testmuai.com")
        main_page = MainPage(driver)
        main_page.wait_for_dom_ready()
        main_page.scroll_to_explore_agentic()
        
        original_window = driver.current_window_handle
        main_page.click_explore_agentic()
        time.sleep(3)
        
        window_handles = driver.window_handles
        print(f"\n[Handles Found]: {window_handles}")
        
        for handle in window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break

        assert "agentic" in driver.current_url.lower() or "testmuai.com" in driver.current_url, f"Unexpected target URL: {driver.current_url}"

        agentic_page = AgenticCloudPage(driver)
        agentic_page.scroll_to_heading()
        agentic_page.click_try_now_free()
        time.sleep(3)

        expected_title = "Sign up for free | Cross Browser Testing Tool"
        assert expected_title in driver.title or "Sign up" in driver.title, f"Title verification failed: Got '{driver.title}'"

        driver.close()
        driver.switch_to.window(original_window)
        print(f"\n[Remaining Window Count]: {len(driver.window_handles)}")

        driver.get("https://testmuai.comblog")
        blog_page = BlogPage(driver)
        blog_page.click_community()
        time.sleep(3)
        assert "://testmuai.com" in driver.current_url, f"Community URL failed: {driver.current_url}"

        driver.execute_script("lambda-status=passed")

    except Exception as error:
        driver.execute_script("lambda-status=failed")
        raise error
    finally:
        driver.quit()
