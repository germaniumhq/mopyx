Feature: If a task fails and removes all the task, previous tasks
    waiting in deduplication should resume execution.

@1
Scenario: Run a process that deduplicates and fails in the process
  Given I run adhesive on 'processes/bugs/deduplicate_multiple_downstream_calls'
  Then the adhesive process has passed


