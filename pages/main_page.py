from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.explore_agentic_link = (By.XPATH, "//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore agentic clouds') or contains(@href, 'agentic-cloud') or contains(@href, 'agentic')]")

    def wait_for_dom_ready(self):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def scroll_to_explore_agentic(self):
        element = self.wait.until(EC.presence_of_element_located(self.explore_agentic_link))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element

    def click_explore_agentic(self):
        target_url = 'https://www.testmuai.com/agentic-cloud/'
        current = self.driver.current_window_handle
        self.driver.execute_script(f"window.open('{target_url}', '_blank');")
        self.wait.until(lambda d: len(d.window_handles) > 1)
        new_handles = [h for h in self.driver.window_handles if h != current]
        self.driver.switch_to.window(new_handles[0])
        self.wait.until(lambda d: 'agentic-cloud' in d.current_url.lower() or 'agentic' in d.current_url.lower())
        return self.driver.current_url
