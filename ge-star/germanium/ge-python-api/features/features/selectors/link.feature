Feature: link selector.

@1
Scenario: Find a link that contains some text.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/link.html'
    When I look for a link with some text: 'some text'
    Then I find the element with id: 'someTextExtra'

@2
Scenario: Find a link that contains exactly some text.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/link.html'
    When I look for a link with exactly the text: 'some text'
    Then I find the element with id: 'someTextExactly'

@3
Scenario: Find a link that has a specific href.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/link.html'
    When I look for a link with the href: 'http://ciplogic.com/'
    Then I find the element with id: 'someTextHref'

@4
Scenario: Find a link that has a href containing some string.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/link.html'
    When I look for a link with the href containing: 'ciplogic'
    Then I find the element with id: 'someTextHref'
