Feature: Login

  Background:
    Given I open the login page

  Scenario Outline: Login with multiple user types
    When I login as "<user_type>"
    Then I should see a "<result>" outcome

    Examples:
      | user_type | result        |
      | standard  | success       |
      | locked    | locked        |
      | invalid   | epic sadface  |
