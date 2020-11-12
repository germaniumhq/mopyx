Feature: Positional access to elements.

  @1 @noie8
  Scenario Outline: clicking on the <Point Location> works as expected (<Div Id>)
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/position/position.html'
    When I click on the <Point Location> of '<Div Id>'
    Then the text of the '#messagesDiv' is '<Expected Message>'
    Examples:
      | Div Id       | Point Location | Expected Message       |
      | #inlineDiv   | exact element  | inline x: 149 y: 100   |
      | #absoluteDiv | exact element  | absolute x: 149 y: 100 |
      | #inlineDiv   | center         | inline x: 150 y: 100   |
      | #absoluteDiv | center         | absolute x: 150 y: 100 |


  @2 @noie8
  Scenario Outline: clicking on the <Point Location> works as expected (<Div Id>)
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/position/position.html'
    When I click on the <Point Location> of '<Div Id>'
    Then the text of the '#messagesDiv' is '<Expected Message>'
    Examples:
      | Div Id       | Point Location | Expected Message     |
      | #inlineDiv   | top left       | inline x: 0 y: 0     |
      | #absoluteDiv | top left       | absolute x: 0 y: 0   |
      | #inlineDiv   | top center     | inline x: 150 y: 0   |
      | #absoluteDiv | top center     | absolute x: 150 y: 0 |
      | #inlineDiv   | top right      | inline x: 299 y: 0   |
      | #absoluteDiv | top right      | absolute x: 299 y: 0 |

  @2 @noie8
  Scenario Outline: clicking on the <Point Location> works as expected (<Div Id>)
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/position/position.html'
    When I click on the <Point Location> of '<Div Id>'
    Then the text of the '#messagesDiv' is '<Expected Message>'
    Examples:
      | Div Id       | Point Location | Expected Message       |
      | #inlineDiv   | middle left    | inline x: 0 y: 100     |
      | #absoluteDiv | middle left    | absolute x: 0 y: 100   |
      | #inlineDiv   | middle right   | inline x: 299 y: 100   |
      | #absoluteDiv | middle right   | absolute x: 299 y: 100 |


  @3 @noie8
  Scenario Outline: clicking on the <Point Location> works as expected (<Div Id>)
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/position/position.html'
    When I click on the <Point Location> of '<Div Id>'
    Then the text of the '#messagesDiv' is '<Expected Message>'
    Examples:
      | Div Id       | Point Location | Expected Message       |
      | #inlineDiv   | bottom left    | inline x: 0 y: 199     |
      | #absoluteDiv | bottom left    | absolute x: 0 y: 199   |
      | #inlineDiv   | bottom center  | inline x: 150 y: 199   |
      | #absoluteDiv | bottom center  | absolute x: 150 y: 199 |
      | #inlineDiv   | bottom right   | inline x: 299 y: 199   |
      | #absoluteDiv | bottom right   | absolute x: 299 y: 199 |
