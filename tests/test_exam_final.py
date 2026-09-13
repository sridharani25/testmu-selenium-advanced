import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

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
    {"browser": "MicrosoftEdge", "version": "127.0", "platform": "macOS Ventura", "build": "Scenario 2 - Edge"},
]


@pytest.mark.parametrize("config", CONFIGURATIONS)
def test_testmu_advanced_assignment(config):
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")

    if not username or not access_key:
        pytest.fail("Credentials missing from .env file!")

    grid_url = "https://hub.lambdatest.com/wd/hub"
    options = ChromeOptions() if config["browser"] == "Chrome" else EdgeOptions()
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
        "console": True,
    }
    options.set_capability("LT:Options", lt_options)

    driver = webdriver.Remote(command_executor=grid_url, options=options)
    driver.set_page_load_timeout(25)
    wait = WebDriverWait(driver, 25)

    try:
        driver.get("https://www.testmuai.com/")
        main_page = MainPage(driver)
        main_page.wait_for_dom_ready()
        main_page.scroll_to_explore_agentic()

        original_window = driver.current_window_handle
        main_page.click_explore_agentic()
        assert "agentic-cloud" in driver.current_url.lower() or "agentic" in driver.current_url.lower(), f"Unexpected target URL: {driver.current_url}"

        agentic_page = AgenticCloudPage(driver)
        agentic_page.scroll_to_heading()
        agentic_page.click_try_now_free()

        title = driver.title.lower()
        expected_title_fragments = [
            "sign up for free",
            "register to your account",
            "sign up",
            "cross browser testing tool",
        ]
        assert any(fragment in title for fragment in expected_title_fragments), f"Title verification failed: Got '{driver.title}'"

        try:
            driver.close()
        except Exception:
            pass
        wait.until(lambda d: len(d.window_handles) >= 1)
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])

        driver.get("https://www.testmuai.com/blog")
        blog_page = BlogPage(driver)
        blog_page.click_community()
        wait.until(lambda d: "community.testmuai.com" in d.current_url.lower())
        assert "community.testmuai.com" in driver.current_url.lower(), f"Community URL failed: {driver.current_url}"

        driver.execute_script("lambda-status=passed")

    except Exception as error:
        try:
            driver.execute_script("lambda-status=failed")
        except Exception:
            pass
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass


def run_parallel_browsers():
    with ThreadPoolExecutor(max_workers=len(CONFIGURATIONS)) as executor:
        futures = [executor.submit(test_testmu_advanced_assignment, config) for config in CONFIGURATIONS]
        for future in as_completed(futures):
            future.result()


if __name__ == "__main__":
    run_parallel_browsers()
