import time

class CartHelper:

    def add_first_n(self, context, n: int) -> None:
        # ALWAYS open products page first
        context.pages.products.open()
        context.pages.products.wait_until_loaded()
        context.pages.products.add_first_n_items(n)

    def get_cart_count_from_badge(self, context) -> int:
        return context.pages.products.get_cart_count()

    def assert_cart_badge(self, context, expected: int) -> None:
        actual = 0
        for _ in range(10):
            actual = self.get_cart_count_from_badge(context)
            if actual == expected:
                return
            time.sleep(0.2)

        raise AssertionError(f"Expected cart badge {expected}, but got {actual}")

    def remove_n_items(self, context, n: int) -> None:
        for _ in range(n):
            context.pages.cart.remove_first_item()
            time.sleep(0.2)

    def validate_item_count_in_cart(self, context, expected: int) -> None:
        actual = None
        for _ in range(10):
            actual = context.pages.cart.get_item_count()
            if actual == expected:
                return
            time.sleep(0.2)

        raise AssertionError(f"Expected {expected} items, but found {actual}")
