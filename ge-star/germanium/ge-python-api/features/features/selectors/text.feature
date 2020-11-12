Feature: text selector.

@1
Scenario: Find an element that contains some text.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for some text: 'just a simple div'
    Then I find the element with id: 'simpleText'

@2
Scenario: Find an element that contains some text with multiple matches.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for some text: 'multimatch'
    Then I find the element with id: 'multimatchspan'

@3
Scenario: Find an element that contains some text that is formatted:
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for some text: 'some formatted text'
    Then I find the element with id: 'formattedText'

@4
Scenario: Find an element that contains some text that has double quotes.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for some text: 'a "text" with quotes'
    Then I find the element with id: 'textWithQuotes'

@5
Scenario: Find an element that contains some text that has single quotes.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for some text: 'a 'text' with quotes'
    Then I find the element with id: 'textWithSingleQuotes'

@6
Scenario: Finding multiple text elements that match across the document.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for some text in multiple elements: 'text'
    Then I find 7 text elements that match

@7
Scenario: Finding text elements across the document, that contain the exact text.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for the exact text in multiple elements: 'text'
    Then I find 1 text elements that match

@8
Scenario: Finding text elements across the document, that contain the exact text, with trimming.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for the exact trimmed text in multiple elements: 'text'
    Then I find 2 text elements that match

@9
Scenario: Finding text elements across the document, should match inside elements.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for the exact text in multiple elements: 'nested'
    Then I find 2 text elements that match

@10
Scenario: Finding text elements across the document, should match inside elements, and trim nbsps.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/selectors/text.html'
    When I look for the exact trimmed text in multiple elements: 'nested'
    Then I find 4 text elements that match
