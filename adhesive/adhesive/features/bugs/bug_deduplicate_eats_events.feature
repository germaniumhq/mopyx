Feature: Test if deduplication drops some of the events, and executes
    all the deduplicated entries.

@1
Scenario: Run a process that deduplicates two events
  Given I run adhesive on 'processes/bugs/deduplicate_eats_events'
  Then the adhesive process has passed

