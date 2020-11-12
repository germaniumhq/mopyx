Feature: Test if deduplication tracks the downstream tasks.

@1
Scenario: Run a process that deduplicates and looks later in the process
  Given I run adhesive on 'processes/bugs/deduplicate_multiple_downstream_calls'
  Then the adhesive process has passed


