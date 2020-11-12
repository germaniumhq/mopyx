Feature: Using selectors as references, should be possible with the constructor
  It's frustrating having to always add paranthesis, even if it's clear what
  we're referring to. For example if we have an `Element(..).containing(InputText())`,
  it would be nicer to allow passing directly the callable, and let Germanium figure
  it out. `Element(..).containing(InputText)`

@1
Scenario: Reference selectors can be passed also as callables.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/selectors/inside_contains.html'
  When I search for a div element using the InputText class as parameter
  Then I find the element with id: 'inputTextContainer'
