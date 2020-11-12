Feature: Opening a firefox browser works out of the box.

  @1
  Scenario: Open a simple page
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    Then the title of the page equals 'INPUTS Page'

  @2
  Scenario: Use multiple threads for editing
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    Then the I can read from a different thread the title of the page as 'INPUTS Page'
