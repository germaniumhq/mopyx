Feature: OaaS needs to dynamically permit loading and unloading of
  services.

  @1
  Scenario: Dynamically register and unregister a service
    Given I have a process 'A-tagged' dynamically serving the service 'process-name' with a custom 'atag' tag
    And I have a process 'B-tagged' dynamically serving the service 'process-name' with a custom 'btag' tag
    When I try to access the 'process-name' service with a custom 'atag' tag
    Then I get back 'A-tagged' from oaas
    When I try to access the 'process-name' service with a custom 'btag' tag
    Then I get back 'B-tagged' from oaas
    When I unregister the 'process-name' from the 'A-tagged' process
    And I try to access the 'process-name' service with a custom 'atag' tag
    Then I get an exception since there is no process serving 'process-name'
