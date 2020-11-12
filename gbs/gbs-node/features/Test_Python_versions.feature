Feature: The versions for the containers should match correctly
    the expected values.

@1
Scenario: Test node 8
Given I run the docker container for 'germaniumhq/node:8'
When I get the version of the default node command
Then it is version '8.12'
When I run in the container 'which node'
Then I get as output '/usr/local/bin/node'
When I run in the container 'which npm'
Then I get as output '/usr/local/bin/npm'
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

@1
Scenario: Test node 8
Given I run the docker container for 'germaniumhq/node:12'
When I get the version of the default node command
Then it is version '12.4'
When I run in the container 'which node'
Then I get as output '/usr/local/bin/node'
When I run in the container 'which npm'
Then I get as output '/usr/local/bin/npm'
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


