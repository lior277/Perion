Feature: Checkout

  Background:
    Given I am logged in

  Scenario: Complete checkout flow
    And I checkout using CSV data
    Then order summary should be correct
    And I should see a success message
    And I should see no items in the order summary
