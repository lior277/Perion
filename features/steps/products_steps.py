from behave import when, then


@then("each product must have name and price")
def step_validate_products(context):
    products = context.pages.products.extract_products()
    for name, price in products:
        assert name.strip()
        assert price > 0


@when('I sort products by "{key}"')
def step_sort_products(context, key):
    context.pages.products.sort(key)


@then("the products should be sorted ascending")
def step_sorted_lohi(context):
    products = context.pages.products.extract_products()
    prices = [p[1] for p in products]
    assert prices == sorted(prices)


@then("the products should be sorted descending")
def step_sorted_hilo(context):
    products = context.pages.products.extract_products()
    prices = [p[1] for p in products]
    assert prices == sorted(prices, reverse=True)
