from selenium.webdriver.common.by import By
from utils.web_driver_extension import DriverEX


class CheckoutOverviewPage:
    ITEM = (By.CLASS_NAME, "cart_item")
    FINISH = (By.CSS_SELECTOR, '[data-test="finish"]')

    def __init__(self, driver, settings):
        self.driver = driver
        self.settings = settings

    def get_item_count(self):
        items = DriverEX.search_elements(self.driver, self.ITEM)
        return len(items)

    def click_finish(self):
        DriverEX.force_click(self.driver, by=self.FINISH)
