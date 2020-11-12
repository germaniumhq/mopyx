Feature: OaaS should transparently switch calls to a different service
  when the underlying service beneath it dies.

  @1
  Scenario: Switch service
    Given I have a process 'A' serving the service 'process-name'
    When I try to access the 'process-name' service
    Then I get back 'A' from oaas
    When I add a process named 'B' for the 'process-name' service
    And I try to access the 'process-name' service
    Then I still get back 'A' from oaas since I have a persistent connection
    When I stop the 'A' process
    And I try to access the 'process-name' service
    Then I get back 'B' from oaas since 'A' is dead
    When I add back 'A' for the 'process-name' service
    Then I still get back 'B' from oaas since I have a persistent connection
