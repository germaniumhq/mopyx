Feature: Running in the workspace should be able to specify the shell

Scenario: Running custom shells should work as well
  When I run adhesive on 'processes/workspace_run/custom_shell'
  Then the adhesive process has passed


