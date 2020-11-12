Feature: Secrets support
  Secrets are supposed to work both in local, and in
  docker workspaces.

Scenario: A workflow that uses secrets should work as expected
  Given I run adhesive on 'processes/plugins_support'
  Then the adhesive process has passed
