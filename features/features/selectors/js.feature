Feature: XPath Selector

@1
Scenario: Find an input button using JsSelector.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
  When I look for the following js selector: return [ document.getElementById('inputButton') ]
  Then I find the element with id: 'inputButton'

@2
Scenario: Returning a non element list in the locator, raises an exception
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
  When I look for the following js selector: return "invalid result";
  Then it throws an exception

@3
Scenario: Searching for a single element, will find the first element.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
  When I look for the following js single element selector
  """
    return [
      document.getElementById('realButton'),
      document.getElementById('inputButton')
    ];
  """
  Then I find the element with id: 'realButton'

@4
Scenario: Searching that returns null, will be considered an empty list.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/button.html'
  When I look for the following js selector: return null;
  Then I find no element
