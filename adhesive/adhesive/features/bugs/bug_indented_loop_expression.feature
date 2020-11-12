Feature: Test if a loop expression that's indented artificially
  by the BPMN editor is correctly handled. It seems that in some
  cases, the CDATA section is nested in the <loopCondition> node.

@1
Scenario:Run a process with a loop, that has an indented CDATA node inside
  Given I run adhesive on 'processes/bugs/indented_loop_expression'
  Then the adhesive process has passed
