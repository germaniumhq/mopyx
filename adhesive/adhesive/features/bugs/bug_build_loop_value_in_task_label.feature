Feature: Out of order executions aren't happening
    Scenario: When running a complex process with multiple dependencies,
        all the tasks are run in the correct order.
      Given I run adhesive on 'processes/bugs/build_loop_value_in_task_label'
      Then the adhesive process has passed
      And there is in the stdout the text 'it's item a'
      And there is in the stdout the text 'it's item b'
      And there is in the stdout the text 'it's item c'
