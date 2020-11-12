Feature: The versions for the containers should match correctly
    the expected values.

@1
Scenario: Test node 8
Given I run the docker container for 'germaniumhq/ubuntu:18.04'
When I run in the container 'whoami'
Then I get as output 'germanium'
When I run in the container 'id -u'
Then I get as output '1000'
When I run in the container 'id -g'
Then I get as output '1000'
When I run in the container 'echo öäüșțăîâ'
Then I get as output 'öäüșțăîâ'
When I run in the container "bash -c 'echo $HOME'"
Then I get as output '/germanium'

