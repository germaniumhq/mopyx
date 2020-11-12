Feature: BPMN lanes are supported, and allow creating workspaces
    whenever execution tokens are entering the lane. The workspaces are
    kept alive as long as there are tasks that still use them.

@1 @manualtest
Scenario: A lane can keep a docker container up for the required
    commands.
  Given I run adhesive on 'processes/lane/docker'
  Then the adhesive process has passed

@2
Scenario: A lane ran in a loop is not instantiated for the starting of the
    loop event.
  Given I run adhesive on 'processes/lane/parametrized_loop_workspace'
  Then the adhesive process has passed

@3
Scenario: A default lane override, gets a workspace regardless
  Given I run adhesive on 'processes/lane/default_lane'
  Then the adhesive process has passed
  And there isn't in the stdout the text 'Unused lane: @lane(expressions=('default',), code=default_lane)'

@4
Scenario: A lane defined with regex can match multiple lanes
  Given I run adhesive on 'processes/lane/parametrized_lane'
  Then the adhesive process has passed
  And there is in the stdout the text 'created lane java'
  And there is in the stdout the text 'created lane maven'

