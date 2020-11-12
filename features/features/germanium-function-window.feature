Feature: Test the `use_window` function.

Scenario: Test if the window changes the context to the specified window.
    Given I open the browser
    And I go to 'http://localhost:8000/features/test-site/window-inputs.html'
    And I click on '#open-window-link'
    When I select the window with the title 'inputs window'
    And I type 'name1 text' into input.name1
    And I click on '#send-data-to-parent'
    And I select the default window
    Then I wait for the text in '#name1Target' to be 'name1 text'

