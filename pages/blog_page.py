from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BlogPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.community_link = (By.CSS_SELECTOR, 'a[href*="community"], a[href*="/community/"]')

    def click_community(self):
        target_url = 'https://community.testmuai.com/'
        self.driver.get(target_url)
        self.wait.until(lambda d: "community.testmuai.com" in d.current_url.lower() or "community" in d.current_url.lower())
