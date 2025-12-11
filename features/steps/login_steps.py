from behave import given, when, then
from features.steps.helpers.login_helper import LoginHelper

login = LoginHelper()


@given("I am logged in")
def step_logged_in(context):
    user = context.users["standard"]
    context.pages.login.open()
    context.pages.login.login(user["username"], user["password"])
    context.pages.products.wait_until_loaded()


@given("I open the login page")
def step_open_login(context):
    context.pages.login.open()


@when('I login as "{user_type}"')
def step_login_user(context, user_type):
    login.login(context, user_type)


@then('I should see a "{result}" outcome')
def step_verify_login(context, result):
    result = result.lower()

    if result == "success":
        assert context.pages.products.is_loaded(), (
            "Products page did not load after login."
        )
        return

    msg = context.pages.login.get_error().lower()
    assert result in msg, f"Expected '{result}' in error message, but got: {msg}"
