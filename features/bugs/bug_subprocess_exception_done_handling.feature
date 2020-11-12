Feature: Cancelling a bunch of events even in subprocesses
    should get the processing of the futures right even if
    some futures might complete simultaneously.

@1
Scenario: Running a process that cancels 20 tasks in a subprocess
    gets down cleanly.
When I run adhesive on 'processes/bugs/subprocess_exceptions_done_race_conditions'
Then the adhesive process has passed

