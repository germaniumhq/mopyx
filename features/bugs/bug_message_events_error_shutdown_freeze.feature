Feature: A process that listens for messages should do down if
    a critical uncatched exception happens, even if technically
    we still have an event running.

Scenario: An exception should tear down event listeners
When I run adhesive on 'processes/bugs/message_events_error_shutdown_freeze'
Then the adhesive process has failed

