Feature: Button selector.

@1
Scenario: Find an input button.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
    When I look for a button with the text: 'nput Butto'
    Then I find the element with id: 'inputButton'

@2
Scenario: Find an input button with exact text.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
    When I look for a button with the exact text: 'Input Button'
    Then I find the element with id: 'inputButton'

@3
Scenario: Find an input button by name.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
    When I look for a button with the name: 'inputButton'
    Then I find the element with id: 'inputButton'

@4
Scenario: Find a real button.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
    When I look for a button with the text: 'eal Butto'
    Then I find the element with id: 'realButton'

@5
Scenario: Find a real button.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
    When I look for a button with the exact text: 'Real Button'
    Then I find the element with id: 'realButton'

@6
Scenario: Find a real button by name.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
    When I look for a button with the name: 'realButton'
    Then I find the element with id: 'realButton'

@7
Scenario: Find a button that is actually a submit button
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
    When I look for a button with the name: 'submitButton'
    Then I find the element with id: 'submitButton'

@8
Scenario: Not finding elements should be ok.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
    When I look for a button with the text: 'not existing button'
    Then there is no element found
