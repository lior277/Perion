Feature: Cart

  Background:
    Given I am logged in

  Scenario Outline: Add and remove items
    When I add <n> products to the cart
    Then the cart badge should show <n>
    When I open the cart page
    And I remove <remove> product from the cart
    Then the cart should show <expected> items

    Examples:
      | n | remove | expected |
      | 3 | 1      | 2        |
      | 5 | 2      | 3        |
