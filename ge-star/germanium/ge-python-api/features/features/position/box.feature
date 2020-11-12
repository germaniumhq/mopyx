Feature: Test the Box API.

  @1 @noie8
  Scenario: Elements that are not found should be reported nicely
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/position/position.html'
    When I try to get the box positions for a selector that doesn't matches
    Then I get an exception spelling out that my selector didn't matched
    # And not a random JS error :)

  @2 @noie8 @noie9
  Scenario: Table cells have different positions
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/position/box.html'
    When I get the box positions for the first two rows
    Then the positions of the 2 boxes are different
