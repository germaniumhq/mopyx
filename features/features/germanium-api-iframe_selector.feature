Feature: Germanium needs to allow switching the iframe selector
  while the instance is running. This allows in turn having the
  same browser instance reused even if the test changes it.

Scenario: Test if changing the iframe selector works while Germanium still runs.
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/iframe-inputs.html'
  When I search in the default iframe for the 'Just a message in the top frame' text
  Then I find the element with id: 'topFrameMessage'
  When I search for the element '#textInput' in the @iframe named 'custom-iframe'
  Then there is no element found
  When I switch the iframe selector to a custom one that handles 'custom-iframe'
  And I search for the element '#textInput' in the @iframe named 'custom-iframe'
  Then I find in iframe 'custom-iframe' the element with id: 'textInput'
  When when I switch the iframe selector back to the tests one
  And I search for the element '#textInput' in the @iframe named 'custom-iframe'
  Then there is no element found
