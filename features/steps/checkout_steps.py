from behave import given, when, then
from utils.csv_loader import load_first_checkout_row


@given("I have items in the cart")
def step_items(context):
    context.pages.products.add_first_n_items(3)


@when("I go to checkout")
def step_checkout(context):
    context.pages.cart.open()
    context.pages.cart.click_checkout()


@when("I checkout using CSV data")
def step_checkout_csv(context):
    first, last, postal, items = context.pages.data.load_first_checkout_row()
    context.pages.checkout.fill_form(first, last, postal)


@then("order summary should be correct")
def step_order_summary(context):
    context.pages.checkout_overview.validate_order_summary()


@then("I should see a success message")
def step_success_message(context):
    assert context.pages.complete.is_success(), "Success page not shown"


@then("I should see no items in the order summary")
def step_no_items(context):
    assert context.pages.checkout_overview.get_item_count() == 0
