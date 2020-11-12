Feature: child_nodes utility function.
  Using child_nodes a user can fetch all the child nodes of an element.

  @1
  Scenario: Find all the child nodes for a given node.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/child_nodes.html'
    When I get the child nodes for the element 'parentDiv'
    Then I get 5 child nodes: 3 text nodes, a div (#childDiv) and a span (#childSpan)

  @2
  Scenario: Find all the child nodes for a node that has no children
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/child_nodes.html'
    When I get the child nodes for the element 'emptyDiv'
    Then I get back an empty list as child nodes

  @3
  Scenario: Find all the child elements for a given node.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/child_nodes.html'
    When I get only the child elements for the element 'parentDiv'
    Then I get 2 child nodes: a div (#childDiv) and a span (#childSpan)
