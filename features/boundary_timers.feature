Feature: Adhesive should support boundary timers.

Scenario: Running a process with a timer should fire the timer.
  Given I run adhesive on 'processes/timers/boundary/duration_timer'
  Then the adhesive process has passed

Scenario: Running a process with a timer should fire the timer.
  Given I run adhesive on 'processes/timers/boundary/duration_timer_cancel'
  Then the adhesive process has passed

Scenario: Running a process with a timer should fire the timer.
  Given I run adhesive on 'processes/timers/boundary/cycle_timer'
  Then the adhesive process has passed

