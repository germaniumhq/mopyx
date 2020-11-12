Feature: Test if the build process is executed incorrectly
    since we have some loops.

Scenario: Run a process that has multiple connections entering a loop
  Given I run adhesive on 'processes/bugs/wrong_multiple_executions'
  Then the adhesive process has passed

