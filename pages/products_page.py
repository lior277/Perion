from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.web_driver_extension import DriverEX


class ProductsPage:
    INVENTORY_LIST = (By.ID, "inventory_container")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON = (By.ID, "shopping_cart_container")

    def __init__(self, driver, settings):
        self.driver = driver
        self.settings = settings
        self.url = self.settings.base_url() + "inventory.html"

    def open(self):
        self.driver.get(self.url)

    def wait_until_loaded(self):
        timeout = self.settings.timeout()
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.INVENTORY_LIST)
        )

    def add_first_n_items(self, n):
        buttons = DriverEX.search_elements(self.driver, self.ADD_BUTTONS)
        for i in range(n):
            DriverEX.force_click(self.driver, element=buttons[i])

    def get_first_n_prices(self, n):
        items = DriverEX.search_elements(self.driver, self.PRODUCT_ITEMS)
        prices = []
        for i in range(n):
            price_el = items[i].find_element(By.CLASS_NAME, "inventory_item_price")
            prices.append(float(price_el.text.replace("$", "")))
        return prices

    def get_cart_count(self) -> int:
        try:
            badge = DriverEX.search_element(self.driver, self.CART_BADGE)
            return int(badge.text)
        except Exception:
            return 0

    # ------------------------------------------------------
    #  NEW: navigate to cart page
    # ------------------------------------------------------
    def go_to_cart(self):
        cart = DriverEX.search_element(self.driver, self.CART_ICON)
        DriverEX.force_click(self.driver, element=cart)
