Feature: Missing steps should be reported

@1
Scenario: A build process that runs a task in parallel
  Given I run adhesive on 'processes/bugs/missing_step_in_subprocess'
  Then the adhesive process has failed
  And there is in the stdout the text 'Missing tasks implementations.'
  And there is in the stdout the text 'def not_existing'

