Project archer is a program that allows easy switching between different
things such as projects, servers, application servers by changing the
current shell.

Installation
============

.. code:: sh

    pip3 install project-archer

Configuration
=============

In order to define a new type of a resource, let’s say a ``project``,
you need first to configure in your ``.bashrc`` the following:

.. code:: sh

    eval "$(archer project)"

This defines a new function in the shell called ``project``. Using this
command you’re able to manage the projects, as well as changing to the
current one.

i.e. on my machine:

.. code:: text

    Available projects:
     - mopyx.yml: mopyx
     - gsb.yml: Germanium Selector Builder
     ...
     - lic.yml: Germanium Licenses
     - gsr.yml: Germanium Star - Runner
    Current project: <none>

In order to create a new project just run:

.. code:: sh

    project -n test

This opens the currently configured editor in the ``$EDITOR`` shell
variable, and in there define what happens when switching to that
project. This file is created in ``~/.archer/projects/test.yml``

.. code:: yaml

    config:
      name: Some descriptive name of your project
      layouts:
      - maven
      exports:
        VAR1: value
      requires:
      - JAVA_HOME
      commands:
        command1: |
          ls -l ...
        command2: |
          # do something else
          pwd
      activate: |
        # this script runs only once after this project is selected
        ..
      deactivate: |
        # this script runs when switching to another project
        ..

Layouts have the same structure, and hold common ``activate``,
``deactivate``, ``exports`` and ``commands`` that are used over multiple
projects. By just pointing to the ``layout`` all the scripts are being
mixed into the current project definition. Having a ``requires``
enforces some environment variables to be present before switching to
the other project.

Layouts have the same structure, except they reside in
``~/.archer/projects/layouts/*.yml``.

The variables that are exposed into the ``exports`` are exported in the
current shell.

Each of the ``commands`` is wrapped into a shell function and available
for execution.

Example Maven Layout
====================

.. code:: yaml

    layout:
        name: maven
        requires: [ PROJECT_HOME ]
        exports:
            PROJECT_BUILD_FOLDER: target/
            MAVEN_OPTS: -Xmx2048m
        commands:
            build: |
                CURRENT_FOLDER=$(pwd)
                cd $PROJECT_HOME
                mvn install $@ $EXTRA_MAVEN_PARAMS
                cd $CURRENT_FOLDER
            clean: |
                CURRENT_FOLDER=$(pwd)
                cd $PROJECT_HOME
                mvn clean $@ $EXTRA_MAVEN_PARAMS
                cd $CURRENT_FOLDER
            test: |
                CURRENT_FOLDER=$(pwd)
                cd $PROJECT_HOME
                mvn test $@ $EXTRA_MAVEN_PARAMS
                cd $CURRENT_FOLDER
            cdproj: |
                cd $PROJECT_HOME
            rebuild: |
                clean && build $@

And a sample project let’s say called ``lic.yml``:

.. code:: yaml

    config:
      name: Germanium Licenses
      layouts:
        - maven
      exports:
        PROJECT_HOME: /home/raptor/projects/germanium-license
      activate: |
        cdproj

When calling ``project lic``, the project gets activated, our current
folder gets automatically changed to
``/home/raptor/projects/germanium-license``, and in the current shell we
have now defined the commands, ``build``, ``clean``, ``test``,
``cdproj`` and ``rebuild`` that execute from any folder we’re in the
maven builds.

To have another maven project, means now just having another file
pointing to the different ``PROJECT_HOME``.

The commands are defined per domain of a problem, and when switching to
another project, the old commands, and all associated environment
variables are undefined.

This also makes sense to start combining them, for example having a
``server`` and a ``project`` definition and testing two projects against
tow application servers becomes:

.. code:: sh

    project A
    rebuild
    serverstop                              # we stop whatever tomcat my be active
    server tomcat7
    redeploy && serverstart                 # test on tomcat 7
    serverstop                              # we stop the current tomcat
    server tomcat8
    redeploy && serverstart                 # test on tomcat 8
    serverstop                              # we stop the current tomcat
    # we go now on testing project B
    project B
    rebuild
    server tomcat7
    redeploy && serverstart                 # test on tomcat 7
    serverstop                              # we stop the current tomcat
    server tomcat8
    redeploy && serverstart                 # test on tomcat 8

Whenever in doubt a call to either ``project`` or ``server`` shows the
list of available servers, and projects, and the active server and
project.

Note that everything becomes far more easier, since we don’t need to
move around ``war`` files, search for running tomcats, and restarting
services manually, cleaning up old things. etc.

Here’s actual layouts that I use for the `tomcat-server`_ and the `maven
project`_.

.. _tomcat-server: https://raw.githubusercontent.com/bmustiata/dotfiles/master/.archer/servers/layouts/tomcat-server.yml
.. _maven project: https://raw.githubusercontent.com/bmustiata/dotfiles/master/.archer/projects/layouts/maven.yml
