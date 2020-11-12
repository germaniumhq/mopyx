Feature: Allow finding table rows in an easy way, fast.
  This internally will construct a single XPath selector, for all the
  given children.

@1
Scenario: I can find table rows with multiple column checks.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/tablerow.html'
  When I search for a TableRow with a CheckBox left of text "Surname"
  Then I find the element with id: 'row2'

@2
Scenario: I can find table rows with multiple xpath selectors.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/tablerow.html'
  When I search for a TableRow with a Button that has label 'edit'
  Then I find the element with id: 'row3'

@3
Scenario: I can find table rows with xpath selectors that have xpath:// in the path.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/tablerow.html'
  When I search for a TableRow with a custom XPath that is //input[@id='nameInput']
  Then I find the element with id: 'row1'
