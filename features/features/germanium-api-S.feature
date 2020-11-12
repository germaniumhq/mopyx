Feature: The S super locator, that returns deferred locators.

@1
Scenario: Find by inferred CSS locators.
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    Then I type 'input test' into input
    Then the value for the input is 'input test'

@2
Scenario: Find by inferred XPath locators.
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    Then I type 'input test' into //input
    Then the value for the //input is 'input test'

@3
Scenario: Find by javascript locators.
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    Then I type 'input test' into js:return [ document.getElementById('textInput') ]
    Then the value for the #textInput is 'input test'

@4
Scenario: Finding elements that don't exist should not throw exceptions
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    And I search using S for //does/not/exist
    And I search using S for div.what
    And I search using S for div["what"].what
    Then nothing happens

@5
Scenario: Element (not)exists(visible) should function.
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    Then the selector '.textInput' exists somewhere
    And the selector '.textInput' exists and is visible
    And the selector '.displayHidden' exists somewhere
    And the selector '.displayHidden' doesn't exists as visible
    And the selector '.missingLocator' doesn't exists at all
    And the selector '.missingLocator' doesn't exists as visible

@6
Scenario: Calling S with an existing locator should return the existing locator.
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    And I search using a nested locator for '#outsideTextFlowedInput'
    Then I find the element with id: 'outsideTextFlowedInput'

@7
Scenario: Calling S with a callable should invoke the callable, and re-eval S.
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    And I search using a callable that returns a CssSelector '#outsideTextFlowedInput'
    Then I find the element with id: 'outsideTextFlowedInput'

@8
Scenario: Elements that are evaluated outside the page with is_displayed should not throw
    The problem happens when the page changes, and we're stuck inside
    a `wait` loop, since we get a page change happening in the background
    while we're still trying to eval elements if they are visible.
    Given I open the browser
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    And I create a StaticElementLocator with a single element: #outsideTextFlowedInput
    Then the StaticElementLocator has one element
    # I invalidate the element in the StaticLocator
    When I go to 'http://localhost:8000/features/test-site/inputs.html'
    Then the StaticElementLocator has no elements anymore

@9
Scenario: Calling S and getting the element_list should allow fetching items by index.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/inputs.html'
    When I search for the 3rd element that is an 'input'
    Then I find the element with id: 'passwordInputField'
