Feature: Executing tests that loop over list with a single element,
    should still loop over that one element.

Scenario: Run a process that has a loop in it with some parallelism
Given I run adhesive on 'processes/bugs/loop_not_executing'
Then the adhesive process has passed

