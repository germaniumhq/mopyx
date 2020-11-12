Feature: OaaS clients should be able to report non-functional
  clients so they can be unregistered from the registry

  @1
  Scenario: Unregister failing service
    Given I have a process 'A' serving the service 'process-name'
    And the 'process-name' is registered in the registry
    When I try to access the 'process-name' service
    Then I get back 'A' from oaas
    When I stop the 'A' process
    And I try to access the 'process-name' service
    Then I get an exception since there is no process serving 'process-name'
    And the 'process-name' is not registered anymore in the registry
