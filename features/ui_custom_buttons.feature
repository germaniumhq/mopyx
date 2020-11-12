Feature: Custom buttons are able to be created in the form.

@manualtest
Scenario: Capturing the stdout should work in a docker task
When I run adhesive without UI redirection on 'processes/multiple_buttons'
Then the user task renders just fine
