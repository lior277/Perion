from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.web_driver_extension import DriverEX


class LoginPage:

    URL = "https://www.saucedemo.com/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")

    INVENTORY_CONTAINER = (By.ID, "inventory_container")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login(self, username: str, password: str):
        """Enter credentials, click login, and wait until redirected to products page."""
        DriverEX.send_keys_auto(self.driver, self.USERNAME, username)
        DriverEX.send_keys_auto(self.driver, self.PASSWORD, password)
        DriverEX.force_click(self.driver, self.LOGIN_BTN)

        # 🚀 CRITICAL FIX: Wait until user is fully logged in and inventory is visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.INVENTORY_CONTAINER)
        )

    def get_error(self) -> str:
        elems = DriverEX.search_elements(self.driver, self.ERROR_MSG)
        return elems[0].text if elems else ""
