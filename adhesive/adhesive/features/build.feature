Feature: build support
    In order to create processes without a definition, just having the
    definitions of the tasks should assemble a very simple linear process.

@1
Scenario: A build process that runs a task in parallel
  Given I run adhesive on 'processes/build/build_loop'
  Then the adhesive process has passed

@2
Scenario: A build process can start tasks in a lane
  Given I run adhesive on 'processes/build/build_lane'
  Then the adhesive process has passed

@3
Scenario: A build process that runs a task after a loop
  Given I run adhesive on 'processes/build/build_loop_task_after'
  Then the adhesive process has passed

@4
Scenario: A programmatic workflow that runs a task in a loop in a custom lane
  Given I run adhesive on 'processes/build/build_loop_lane'
  Then the adhesive process has passed

@5
Scenario: A task that contains regex characters can still be created
  Given I run adhesive on 'processes/build/build_generate_names_with_re'
  Then the adhesive process has passed

