Feature: Unused tasks and lanes should be displayed to help in maintenance of
    code from the BPMN diagram to the definition of the code.

Scenario: Run a workflow with unused tasks and lanes
    When I run adhesive on 'processes/programmatic_unused_task'
    Then the adhesive process has passed
    And there is in the stdout the text 'Unused task: @task(expressions=('Not Used Task',), code=not_used_task)'
    And there is in the stdout the text 'Unused usertask: @usertask(expressions=('Not Used UserTask',), code=not_used_user)'
    And there is in the stdout the text 'Unused lane: @lane(expressions=('Not Used Lane',), code=not_used_lane)'
    And there isn't in the stdout the text 'Unused task: @task(expressions=('Used Task',), code=used_task)'
    And there isn't in the stdout the text 'Unused lane: @lane(expressions=('Used Lane',), code=used_lane)'

