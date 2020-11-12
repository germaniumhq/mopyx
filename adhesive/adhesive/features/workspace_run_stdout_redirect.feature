Feature: STDOUT can be captured when running tasks

Scenario: Capturing the stdout should work in a task
  When I run adhesive on 'processes/workspace_run/stdout_capture'
  Then the adhesive process has passed

@manualtest
Scenario: Capturing the stdout should work in a docker task
  When I run adhesive on 'processes/workspace_run/stdout_capture_docker'
  Then the adhesive process has passed
