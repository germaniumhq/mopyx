Feature: inside/containing feature check for selectors.

@1
Scenario: I can find elements inside a specific element.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for an InputText inside the div with id inputTextContainer
  Then I find the element with id: 'inputText'

@2
Scenario: I can find elements inside a specific element using CSS.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search using CSS for an input inside the div#inputTextContainer
  Then I find the element with id: 'inputText'

@3
Scenario: Finding elements inside non CSS/XPath locators returns correctly
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a div inside a JS selector
  Then I find the element with id: 'inputTextContainer'

@4
Scenario: I can find elements that contain specific elements.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a div containing an InputText
  Then I find the element with id: 'inputTextContainer'

@5
Scenario: I can find elements that contain specific elements using CSS.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search using CSS for a div containing an InputText
  Then I find the element with id: 'inputTextContainer'

@6
Scenario: Finding elements containing CSS/XPath locators is working correctly.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a div containing a JS selector
  Then I find the element with id: 'inputTextContainer'

@7
Scenario: Finding elements without children should find only those that actually have no children
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for all the divs without children
  Then I only get the div with id #decoyDiv

@8
Scenario: Finding elements without children might also return no elements, even if there are elements with children
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for all the spans without children
  Then I get no elements returned

@9
Scenario: Finding elements using indexes should construct the correct XPath
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for the first input in the second div
  Then I find the element with id: 'inputText'

@10
Scenario: Finding elements that contain _ALL_ the searched internal elements works correctly.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a div that contains both an input and a span
  Then I find the element with id: 'inputTextWithOtherDivContainer'

@11
Scenario: Finding elements that contain selectors that don't return anything, yields nothing.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a div that contains a span, that contains a text 'missing text'
  Then I get no elements returned

@12
Scenario: Finding elements that contain selectors that do return, will return correctly.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a div that contains a span, that contains a text 'text inside divs and spans'
  Then I find the element with id: 'divContainingASpanAndAnotherSpan'

@13
Scenario: Finding elements that contain invisible elements, will return correctly.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a div that contains a br
  Then I find the element with id: 'divWithABr'

@14
Scenario: Finding elements that use an inside reference a WebElement, will work
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for an InputText inside the div element with id inputTextContainer
  Then I find the element with id: 'inputText'

@15
Scenario: I can find elements outside an element
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a span outside a div
  Then I find the element with id: 'justATrailingSpanOutsideDivs'
