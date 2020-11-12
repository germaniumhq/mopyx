Feature: The versions for the containers should match correctly
    the expected values.

Scenario: Test java 1.8
Given I run the docker container for 'germaniumhq/jdk:8'
When I get the version of the default java command
Then I get as version '1.8.0'
When I run in the container 'which java'
Then I get as output '/usr/bin/java'
When I run in the container 'which javac'
Then I get as output '/usr/bin/javac'
When I run in the container 'which mvn'
Then I get as output '/usr/bin/mvn'
When I run in the container 'whoami'
Then I get as output 'germanium'
When I run in the container 'echo öäüșțăîâ'
Then I get as output 'öäüșțăîâ'
When I run in the container "bash -c 'echo $HOME'"
Then I get as output '/germanium'

