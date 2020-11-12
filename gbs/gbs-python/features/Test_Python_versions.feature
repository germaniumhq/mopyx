Feature: The versions for the containers should match correctly
    the expected values.

@1
Scenario: Test python 2.7
Given I run the docker container for 'germaniumhq/python:2.7'
When I get the version of the default python command
Then it is version '2.7'
When I run in the container 'which python'
Then I get as output '/python/bin/python'
When I run in the container 'which pip'
Then I get as output '/python/bin/pip'
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

@3
Scenario: Test python 3.5
Given I run the docker container for 'germaniumhq/python:3.5'
When I get the version of the default python command
Then it is version '3.5'
When I run in the container 'which python'
Then I get as output '/python/bin/python'
When I run in the container 'which pip'
Then I get as output '/python/bin/pip'
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

@4
Scenario: Test python 3.6
Given I run the docker container for 'germaniumhq/python:3.6'
When I get the version of the default python command
Then it is version '3.6'
When I run in the container 'which python'
Then I get as output '/python/bin/python'
When I run in the container 'which pip'
Then I get as output '/python/bin/pip'
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

@5
Scenario: Test python 3.7
Given I run the docker container for 'germaniumhq/python:3.7'
When I get the version of the default python command
Then it is version '3.7'
When I run in the container 'which python'
Then I get as output '/python/bin/python'
When I run in the container 'which pip'
Then I get as output '/python/bin/pip'
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

@6
Scenario: Test python 3.8
Given I run the docker container for 'germaniumhq/python:3.8'
When I get the version of the default python command
Then it is version '3.8'
When I run in the container 'which python'
Then I get as output '/python/bin/python'
When I run in the container 'which pip'
Then I get as output '/python/bin/pip'
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

@7
Scenario: Test miniconda python 3.6
Given I run the docker container for 'germaniumhq/python:3.6-win32'
When I get the version of the miniconda python command
Then it is version '3.6'
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

