Feature: parent_node utility function
  parent_node is an utility function that allows fetching the
  parentNode fo a given element.

  Scenario: parent_node utility function
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/parent_node.html'
    When I get the parent node of the element with id 'childDiv'
    Then I find the element with id: 'expectedParent'
