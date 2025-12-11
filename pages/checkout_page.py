from selenium.webdriver.common.by import By
from utils.web_driver_extension import DriverEX


class CheckoutPage:
    FIRST = (By.ID, "first-name")
    LAST = (By.ID, "last-name")
    POSTAL = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    ERROR_MSG = (By.CSS_SELECTOR, '[data-test="error"]')

    def __init__(self, driver, settings):
        self.driver = driver
        self.settings = settings

    def fill_form(self, first, last, postal):
        DriverEX.send_keys_auto(self.driver, self.FIRST, first)
        DriverEX.send_keys_auto(self.driver, self.LAST, last)
        DriverEX.send_keys_auto(self.driver, self.POSTAL, postal)
        DriverEX.force_click(self.driver, by=self.CONTINUE)

    def click_continue(self):
        DriverEX.force_click(self.driver, by=self.CONTINUE)

    def has_error(self):
        return len(DriverEX.search_elements(self.driver, self.ERROR_MSG)) > 0

    def get_error(self):
        elems = DriverEX.search_elements(self.driver, self.ERROR_MSG)
        return elems[0].text if elems else ""
