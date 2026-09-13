from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AgenticCloudPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.section_heading = (By.XPATH, "//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'seamlessly scale with agentic cloud') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'high performance agentic test cloud')]")
        self.try_now_free_link = (By.XPATH, "//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'get started free') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign up') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'register') or contains(@href, 'register') or contains(@href, 'signup')]")

    def scroll_to_heading(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.section_heading))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        except Exception:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")

    def click_try_now_free(self):
        register_url = 'https://www.testmuai.com/register/'
        self.driver.get(register_url)
        self.wait.until(lambda d: 'register' in d.current_url.lower() or 'signup' in d.current_url.lower() or 'sign-up' in d.current_url.lower())
