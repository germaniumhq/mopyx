Feature: Simple Element Locator found elements should function with send_keys
  It seems that when an element was found , sending
  keys to it doesn't functions as expected.

  Scenario:
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    Then I type 'input test' into input
    Then the value for the input is 'input test'

