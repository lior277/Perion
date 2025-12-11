from behave.runner import Context
from features.steps.helpers.cart_helper import CartHelper
from features.steps.helpers.data_helper import DataHelper
from features.steps.helpers.login_helper import LoginHelper


class BaseSteps:
    def __init__(self) -> None:
        self.login = LoginHelper()
        self.cart = CartHelper()
        self.data = DataHelper()

    def assert_url_contains(self, context: Context, text: str) -> None:
        assert text in context.driver.current_url, (
            f"Expected '{text}' in URL, got: {context.driver.current_url}"
        )
