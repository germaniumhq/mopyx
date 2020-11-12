Feature: Using germanium should be easy to right click, click or double click.
    When having a WebDriver object it's pretty tricky to do
    basic operations such as right click or click. For example
    clicking on an element can easily be done via `element
    .click()`, but for doing a right click it becomes necessary
    to create an ActionChain, and then pass the element into the
    ActionChain.

@1
Scenario: Basic click
      Given I open the browser
      And I go to 'http://localhost:8000/features/test-site/mouse.html'
      When I click on '.eventTargetDiv'
      Then the value for the input#textInput is 'click'

@2
Scenario: Right click
      Given I open the browser
      And I go to 'http://localhost:8000/features/test-site/mouse.html'
      When I right click on .eventTargetDiv
      Then the value for the input#textInput is 'contextmenu'

@3
Scenario: Double click
      Given I open the browser
      And I go to 'http://localhost:8000/features/test-site/mouse.html'
      When I doubleclick on .eventTargetDiv
      Then the value for the input#textInput is 'doubleclick'

@4
Scenario: Hover over
      Given I open the browser
      And I go to 'http://localhost:8000/features/test-site/mouse.html'
      When I mouse over on .eventTargetDiv
      Then the value for the input#textInput is 'mouseover'

@5
Scenario: Hover with scrolling and clicks should work.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/mouse.html'
  When I mouse over on .bottomDiv
  And I mouse over on .farDownElementInThePage
  And I click on '.buttonAboveFarDownElementInThePage'
  Then the value for the input#textInput is 'click:buttonAboveFarDownElementInThePage'

@6
Scenario: Using another mouse action (click) should send a mouse out for hovered elements
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/mouse.html'
  When I mouse over on .buttonAboveFarDownElementInThePage
  And I click on '.bottomDiv'
  Then the value for the input#textInput is 'mouseout:buttonAboveFarDownElementInThePage'

@7
Scenario: Using another mouse action (right click) should send a mouse out for hovered elements
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/mouse.html'
  When I mouse over on .buttonAboveFarDownElementInThePage
  And I right click on .bottomDiv
  Then the value for the input#textInput is 'mouseout:buttonAboveFarDownElementInThePage'

@8
Scenario: Using another mouse action (mouse over) should send a mouse out for hovered elements
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/mouse.html'
  When I mouse over on .buttonAboveFarDownElementInThePage
  And I mouse over on .bottomDiv
  Then the value for the input#textInput is 'mouseout:buttonAboveFarDownElementInThePage'
