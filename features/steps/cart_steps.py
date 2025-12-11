from behave import when, then, given
from features.steps.helpers.cart_helper import CartHelper

cart = CartHelper()

@given("I have an empty cart")
def step_empty_cart(context):
    context.pages.cart.open()
    while context.pages.cart.get_item_count() > 0:
        context.pages.cart.remove_first_item()

@when("I add {n:d} products to the cart")
def step_add_products(context, n):
    cart.add_first_n(context, n)


@then("the cart badge should show {count:d}")
def step_cart_badge(context, count):
    cart.assert_cart_badge(context, count)


@when("I open the cart page")
def step_open_cart(context):
    context.pages.products.go_to_cart()


@when("I remove {n:d} products from the cart")
@when("I remove {n:d} product from the cart")
def step_remove_products(context, n):
    cart.remove_n_items(context, n)


@then("the cart should show {count:d} items")
def step_cart_items(context, count):
    cart.validate_item_count_in_cart(context, count)
