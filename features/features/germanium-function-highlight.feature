Feature: highlight utility function.
  The user can make an element blink for a number of seconds,
  in order to aid in detecting where the elements are on the page.

@1
Scenario: Check if highlighting works correctly for visible elements without logging.
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/highlight.html'
  And I highlight the element '#visibleDiv'
  Then the highlighted element is '#visibleDiv'

@2
Scenario: Check if highlighting works correctly for visible elements with console.log
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/highlight.html'
  And I highlight also in the console the element '#visibleDiv'
  Then the highlighted element is '#visibleDiv'
  And in the log the highlighted element was notified as found

@3
Scenario: Check if highlighting alerts invisible elements
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/highlight.html'
  And I highlight the element '#invisibleDiv'
  Then there is an alert notifying the element as not visible

@4
Scenario: Check if highlighting with console.log invisible elements works
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/highlight.html'
  And I highlight also in the console the element '#invisibleDiv'
  Then in the log there is an error message notifying the element is invisible
  And there is no alert present

@5
Scenario: Check if highlighting alerts missing elements
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/highlight.html'
  And I highlight the element '#notExistingDiv'
  Then there is an alert notifying the element as non existing

@6
Scenario: Check if highlighting with console.log alerts in the log missing elements
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/highlight.html'
  And I highlight also in the console the element '#notExistingDiv'
  Then in the log there is an error message notifying the element as non existing
  And there is no alert present

@7
Scenario: Check if highlighting the same element twice laves it highlighted
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/highlight.html'
  When I highlight twice the element '#visibleDiv'
  Then the element highlight for the '#visibleDiv' is cleared correctly
