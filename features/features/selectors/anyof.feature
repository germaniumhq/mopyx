Feature: In order to support multiple matches, it makes sense to write
  a selector that would match if any of its sub-selectors match.
  While every AbstractSelector does support a get_selectors() that
  returns multiple String selectors, this approach doesn't allow
  filtering selectors.

@1
Scenario: Find a button implemented with AnyOfSelector
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
  When I look for a custom button selector with the text: 'Input Button'
  Then I find the element with id: 'inputButton'
  When I look for a custom button selector with the text: 'Real Button'
  Then I find the element with id: 'realButton'
  When I look for a custom button selector with the text: 'Submit Button'
  Then I find the element with id: 'submitButton'
