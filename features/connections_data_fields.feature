Feature: Connections should allow in expressions access to data
    fields, except for `loop`, `context`, `workspace` and `data`.


Scenario: Running a workflow with data fields checked on the connection
        works, without having to specify the `data` attribute.
  When I run adhesive on 'processes/connection_data_check'
  Then the adhesive process has passed
