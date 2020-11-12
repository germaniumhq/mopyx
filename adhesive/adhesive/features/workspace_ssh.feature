Feature: SSH workspaces can be executed

@1 @noprocess @manualtest
Scenario: Running some task via SSH should work
  When I run adhesive on 'processes/ssh/workspace_ssh'
  Then the adhesive process has passed

@2 @noprocess @manualtest
Scenario: Running some task via SSH in a lane should work
  When I run adhesive on 'processes/ssh/lane_workspace_ssh'
  Then the adhesive process has passed

@3 @noprocess @manualtest
Scenario: Running user tasks in a SSH lane should work
  When I run adhesive without UI redirection on 'processes/ssh/lane_workspace_usertask_ssh'
  Then the user task renders just fine
