Feature: Germanium waited utility function.
  Whenever we want to do an operation such as:

    click(Input(..))

  It might happen that we need first to have the input appearing.
  Usually the pattern is:

    wait(Input(..))
    click(Input(..))

  To make it simpler, a new function waited() allows us to use the
  wait, and return the select. Thus we can use wait inside ifs, or
  actions such as click with ease:

    click(waited(Input(..))

@1
Scenario: Test simple waited.
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/waited-button.html'
  Then the text of the page doesn't contain 'button clicked'
  And I click on waited 'button'
  Then the text of the page contains 'button clicked'
