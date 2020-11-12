Feature: get_style utility function.
  Using get_style a user can easily query the actual value
  of a CSS property.

  On firefox due to a bug, shortand values can't be used:
  https://bugzilla.mozilla.org/show_bug.cgi?id=137688

@1
Scenario: Check reading CSS values from an element.
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/style.html'
  # the red div checks
  Then the 'borderTopColor' style color from element '.red-div' is '#ff0000'
  And the 'borderTopStyle' style from element '.red-div' is 'solid'
  And the 'borderTopWidth' style from element '.red-div' is '1px'
  And the 'color' style color from element '.red-div' is '#ff0000'
  # and now the default div
  And the 'borderTopColor' style color from element '.default-div' is '#000000'
  And the 'borderTopStyle' style from element '.default-div' is 'none'
  And the 'borderTopWidth' style from element '.default-div' is '0px'
  And the 'color' style color from element '.default-div' is '#000000'

@2
Scenario: Check reading CSS values from an element where the style is set via highlight
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/style.html'
  When I highlight the element '.default-div'
  Then the 'outlineColor' style color from element '.default-div' is '#00ff00'
