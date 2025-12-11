from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class Pages:
    def __init__(self, driver, settings):
        self.driver = driver
        self.settings = settings

        self.login = LoginPage(driver)
        self.products = ProductsPage(driver, settings)
        self.cart = CartPage(driver, settings)
        self.checkout = CheckoutPage(driver, settings)
