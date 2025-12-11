from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from utils.web_driver_extension import DriverEX


class CartPage:
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    REMOVE_BTN = (By.CSS_SELECTOR, ".cart_item button[data-test^='remove']")
    CHECKOUT_BTN = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def __init__(self, driver: WebDriver, settings):
        self.driver = driver
        self.settings = settings
        self.url = self.settings.base_url() + "cart.html"

    def open(self):
        self.driver.get(self.url)

    def get_item_count(self) -> int:
        items = DriverEX.search_elements(self.driver, self.CART_ITEM)
        return len(items)

    def remove_first_item(self) -> None:
        before = self.get_item_count()
        if before == 0:
            return

        items = DriverEX.search_elements(self.driver, self.CART_ITEM, wait_if_empty=True)
        first_item = items[0]

        btn = first_item.find_element(By.CSS_SELECTOR, "button[data-test^='remove']")

        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

        timeout = self.settings.timeout()
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_item_count() < before
        )

    def click_checkout(self):
        btn = DriverEX.search_element(self.driver, self.CHECKOUT_BTN)
        DriverEX.force_click(self.driver, element=btn)
