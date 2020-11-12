Feature: CSS Selector

@1
Scenario: Find an input button using CSS.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
  When I look for the following css selector: #inputButton
  Then I find the element with id: 'inputButton'
