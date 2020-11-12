Feature: The js API.

Scenario: Call a JS Script with a custom argument.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/inputs.html'
    When I execute js with one parameter 'jsparameter'
    """
    if (arguments.length == 0) {
        throw new Error("Expected one argument");
    }

    if (arguments[0] != "jsparameter") {
        throw new Error("The parameter is " + arguments[0] + " instead of `jsparameter`");
    }
    """
    Then nothing happens

Scenario: Call a JS Script that returns a list of elements.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/inputs.html'
    When I execute js without any parameters
    """
    return [
        document.getElementById('textInput'),
        document.getElementById('anotherTextInput')
    ];
    """
    Then I got two elements, one with id textInput, and the other with id anotherTextInput.