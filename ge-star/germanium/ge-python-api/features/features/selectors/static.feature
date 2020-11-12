Feature: Static selectors should allow running conditions
  against elements that we already have.

Scenario: Test if finding a basic static selector works as expected.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/static.html'
  When I have a static selector for the '#staticElement'
  Then the static element locator returns the same element as '#staticElement'

Scenario: Test if finding a static selector with invalid conditions works as expected.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/static.html'
  When I have a static selector for all the '.group-div' elements, including the invisible
  And search the static selector
  Then I find 2 elements that match

Scenario: Test if finding an invisible static selector returns nothing
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/static.html'
  When I have a static selector for the '#staticElement'
  And I search the static selector inside a table
  Then I find no element
  When I have a static selector for the '#staticElementInsideTable'
  And I search the static selector inside a table
  Then I find the element with id: 'staticElementInsideTable'
