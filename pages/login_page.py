from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # 10-second explicit wait

        # Locators (Advanced tip: Keep locators strictly at the top)
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_credentials(self, username, password):
        # Explicitly wait for elements to be visible (Required for Advanced level)
        user_field = self.wait.until(EC.visibility_of_element_located(self.username_input))
        user_field.send_keys(username)
        
        pass_field = self.driver.find_element(*self.password_input)
        pass_field.send_keys(password)

    def click_login(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
        btn.click()
