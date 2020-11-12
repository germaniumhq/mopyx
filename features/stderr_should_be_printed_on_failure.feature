Feature: If a task throws an exception I don't need to drill into the logs folder.


Scenario: Run a workflow that fails with an exception
    When I run adhesive on 'processes/stderror_handling'
    Then the adhesive process has failed
    And there is in the stdout the text 'Custom exception was thrown'
    And there is in the stdout the text 'throw_some_exception'


Scenario: Run a workflow that fails running a redirected program
    When I run adhesive on 'processes/stderror_no_redirect'
    Then the adhesive process has failed
    And there is in the stdout the text 'test'
    And there is in the stdout the text 'subprocess.CalledProcessError: Command'
    And there is in the stdout the text 'false'
