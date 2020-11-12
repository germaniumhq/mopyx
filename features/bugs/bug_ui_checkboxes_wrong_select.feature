Feature: On a UI with a checkbox group, the items should be
    correctly selected.

    @manualtest
    Scenario: Test UI selection of checkboxes.
      Given I run adhesive without UI redirection on 'processes/bugs/ui_checkboxes_wrong_select'
      Then the user task renders just fine

    @manualtest
    Scenario: Test UI selection of checkboxes.
      Given I run adhesive without UI redirection on 'processes/bugs/ui_checkboxes_wrong_select_loop_execution'
      Then the user task renders just fine
