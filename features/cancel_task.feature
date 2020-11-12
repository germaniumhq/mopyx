Feature: cancel task support
    When a task is cancelled it should be stopped immediately

@1
Scenario: A task that cancels the current task in a timer
  Given I run adhesive on 'processes/cancel_boundary/simple'
  Then the adhesive process has passed

@2
Scenario: A task that cancels a subprocess in a timer
  Given I run adhesive on 'processes/cancel_boundary/subprocess'
  Then the adhesive process has passed

@3
Scenario: A task that cancels a nested subprocess in a timer
  Given I run adhesive on 'processes/cancel_boundary/nested-subprocess'
  Then the adhesive process has passed

@4
Scenario: A task that errors, without an error task, gets its error propagated
  Given I run adhesive on 'processes/cancel_boundary/root_error_cancels_everything'
  Then the adhesive process has failed
  And there is in the stdout the text 'Failed Raise Exception'
  And there is in the stdout the text 'Terminated Wait 2 seconds reason'
  And there is in the stdout the text 'Terminated <process> reason'
  And there is in the stdout the text 'Process execution failed. Unhandled error from'
