Feature: Out of order executions aren't happening
    Scenario: When running a complex process with multiple dependencies,
        all the tasks are run in the correct order.
      Given I run adhesive on 'processes/bugs/out_of_order_execution'
      Then the adhesive process has passed
      And the 'bob: srv-core' is executed only once
