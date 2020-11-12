Feature: Germanium wait utility function.
  When waiting for things, we generally wait for an element
  to appear. Unfortunately in many cases what might happen
  is that an error will occur, and our wait will be stuck
  in the waiting until the timeout occurs.

  Thus Germanium provides a wait that can be shortcircuited
  by error conditions, specified via its `while_not`
  attribute.

@1
Scenario: Test simple wait
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/wait-error.html'
  Then waiting for error to happen should pass

@2
Scenario: Test simple while_not callback
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/wait-error.html'
  Then waiting for success to happen should fail

@3
Scenario: Test multiple wait callback as array
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/wait-error.html'
  Then waiting for error or success to happen should pass with array callbacks

@4
Scenario: Test multiple wait callback as vararg
  Given I open the browser
  When I go to 'http://localhost:8000/features/test-site/wait-error.html'
  Then waiting for error or success to happen should pass with multiarg callbacks

@5
Scenario: Test having wait on a closure that returns a closure does the resolving correctly
  When I wait on a closure that returns a closure that returns False
  Then the wait function call failed

@6
Scenario: Test having while_not returning closures, also get resolved recursively.
  When I wait on a while_not that returns a closure that returns False
  Then the wait function call passed

@7
Scenario: Test having while_not returning closures that throw fail the wait.
  When I wait on a while_not that returns a closure that throws
  Then the wait function call failed

@8
Scenario: Waiting on a while_not using the S function should not fail
  Given I open the browser
  And I go to 'http://localhost:8000/features/test-site/wait-error.html'
  When I wait with a while_not that has a CSS locator built with S should pass
