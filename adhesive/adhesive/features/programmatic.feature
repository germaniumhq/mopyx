Feature: Programmatic support
  Adhesive should allow creating workflows with simple
  commands, without having to always read a BPMN file.

@1
Scenario: A programmatic process that runs a task in parallel
  Given I run adhesive on 'processes/programmatic/programmatic_loop'
  Then the adhesive process has passed

@2
Scenario: A programmatic process that runs a task in a lane
  Given I run adhesive on 'processes/programmatic/programmatic_lane'
  Then the adhesive process has passed

@3
Scenario: A programmatic process that runs a looped task in a lane in parallel
  Given I run adhesive on 'processes/programmatic/programmatic_loop_lane'
  Then the adhesive process has passed

@4
Scenario: A programmatic process that skips a task on a when condition
  Given I run adhesive on 'processes/programmatic/programmatic_when_condition'
  Then the adhesive process has passed
