Feature: Products Page

  Background:
    Given I am logged in

  Scenario: Validate product list
    Then each product must have name and price

  Scenario: Sort by lowest price
    When I sort products by "lohi"
    Then the products should be sorted ascending

  Scenario: Sort by highest price
    When I sort products by "hilo"
    Then the products should be sorted descending
