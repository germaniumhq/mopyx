Feature: General Element Selector
  This a selector that will build an XPath selector, allowing
  matches with a simpler syntax.

@1
Scenario: Find some text using the general element selector.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/element.html'
  When I look for a 'div' element with 'is some' text in it
  Then I find the element with id: 'formattedText'

@2
Scenario: Find an element by attributes.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/element.html'
  When I look for a 'div' element with a 'contenteditable=true' attribute
  Then I find the element with id: 'editableDiv'

@3
Scenario: Find an element by a given class name
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/element.html'
  When I look for a 'div' element with class 'formatted-text'
  Then I find the element with id: 'editableText'

@4
Scenario: Find an element by multiple class names
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/element.html'
  When I look for a 'div' element with classes 'formatted-text' and 'formatted-text-extra'
  Then I find the element with id: 'editableText2'

@5
Scenario: Find an element by multiple class names
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/element.html'
  When I look for a 'div' element with class 'formatted-text-extra formatted-text'
  Then I find the element with id: 'editableText2'

@6
Scenario: Find an element by a part of an attribute
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/element.html'
  When I look for a 'div' element with a matching 'contenteditable=ru' attribute
  Then I find the element with id: 'editableDiv'

@7
Scenario: Find an element with an index.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/element.html'
  When I look for the 3rd div element
  Then I find the element with id: 'formattedText'
