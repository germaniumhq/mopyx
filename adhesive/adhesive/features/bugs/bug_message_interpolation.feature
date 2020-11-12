Feature: Messages in the task title should use the context variable
    interpolation.

@1
Scenario: Run a workflow that interpolates messages on the task execution
    When I run adhesive on 'processes/bugs/message_interpolation'
    Then the adhesive process has passed
    And there is in the stdout the text 'Resolved Value'

@2
Scenario: Run a workflow that interpolates dictionary based messages
    When I run adhesive on 'processes/bugs/message_interpolation_events'
    Then the adhesive process has passed
    And there is in the stdout the text 'Event Check Resolved Id'
    And there is in the stdout the text 'Event Execute Resolved Data'


