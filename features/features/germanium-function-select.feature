Feature: Implement selection of elements in <select> HTML objects.
  In regular APIs selecting an element from a Select it's buried deep
  inside webdriver code. It would be nice to have an API that allows
  selecting items with ease, just like a regular action.

@1
Scenario: On a page with a select, I can select its value by its text
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/select.html'
  When I select in the first select the entry with text 'A1'
  Then the value in the first select is 'a1value'

@2
Scenario: On a page with a select, I can select its value by its value
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/select.html'
  When I select in the first select the entry with value 'a2value'
  Then the value in the first select is 'a2value'

@3
Scenario: On a page with a select, I can select its value by its index
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/select.html'
  When I select in the first select the entry with index 3
  Then the value in the first select is 'a3value'

@4 @noedge
Scenario: On a page with a multiline select, I can select its values by texts.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/select.html'
  When I select in the multiline select the entries with texts B1 and B4
  Then the values in the multiline select are 'b1value' and 'b4value'

@5 @noedge
Scenario: On a page with a multiline select, I can select its values by values.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/select.html'
  When I select in the multiline select the entries with values b2value, b4value and b6value
  Then the values in the multiline select are 'b2value', 'b4value' and 'b6value'

@6 @noedge
Scenario: On a page with a multiline select, I can select its values by indexes.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/select.html'
  When I select in the multiline select the entries with indexes 1, 3 and 5
  Then the values in the multiline select are 'b1value', 'b3value' and 'b5value'

@7 @noedge
Scenario: On a page with a multiline select, I can deselect some elements
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/select.html'
  When I select in the multiline select the entries with indexes 1, 3 and 5
  And I deselect in the multiline select the entries with indexes 3 and 5
  And I select in the multiline select the entries with indexes 4
  Then the values in the multiline select are 'b1value' and 'b4value'
