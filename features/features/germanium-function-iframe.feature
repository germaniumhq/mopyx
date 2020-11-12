Feature: Test the `@iframe` decorator.
    Switching, and in general iframe management is pretty painful.
    Germanium allows specifying an iframe strategy, that will be
    used to centralize all the iframe management into only one place.

Scenario: Test if the iframe changes the context to the specified iframe.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/iframe-inputs.html'
    When I type into iframe in input#textInput the following text: input test
    Then in the iframe the value for the input#textInput is 'input test'

#Scenario: Test if the iframe function reports correctly the wrong iframe name
#    Given I open the browser
#    And I go to 'http://localhost:8000/features/test-site/iframe-inputs.html'
#    And I switch the iframe selector to the germanium bundled default selector
#    When I try to access the iframe named 'wrong_iframe' that is not by default defined
#    And when I switch the iframe selector back to the tests one
#    Then the exception message contains the text 'wrong_iframe'

Scenario: parent_node utility function
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/parent_node.html'
    When I get the parent node of the element with id 'childDiv'
    Then I find the element with id: 'expectedParent'
