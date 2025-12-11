from selenium.webdriver.common.by import By
from utils.web_driver_extension import DriverEX


class CompletePage:
    HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')
    SUMMARY_LIST = (By.CSS_SELECTOR, ".cart_item")

    def __init__(self, driver, settings):
        self.driver = driver
        self.settings = settings

    def get_success_message(self) -> str:
        return DriverEX.get_element_text(self.driver, self.HEADER)

    def has_no_items(self) -> bool:
        items = self.driver.find_elements(*self.SUMMARY_LIST)
        return len(items) == 0
