A CI/CD system build around BPMN and Python. Basically a micro BPMN
runner with python step implementations targeted for builds. Able to run
in the terminal.

Installation
============

.. code:: sh

    pip install adhesive

Getting Started
===============

Simple Builds
-------------

To create a basic build you just create a file in your project named
``_adhesive.py``. In it you then declare some tasks. For example:

.. code:: python

    import adhesive

    @adhesive.task("Checkout Code")
    def checkout_code(context):
        adhesive.scm.checkout(context.workspace)

    @adhesive.task("Run Build")
    def run_build(context):
        context.workspace.run("mvn clean install")

    adhesive.build()

Since no process was defined, adhesive takes the defined tasks, stitches
them in order, and has a process defined as ``<start>`` →
``Checkout Code`` → ``Run
Build`` → ``<end>``.

To run it simply call ``adhesive`` in the terminal:

.. code:: sh

    adhesive

This is the equivalent of Jenkins stages. But we can do better:

Programmatic Builds
-------------------

In order to use the full programmatic functionalities that adhesive
offers, you are able to stitch your BPM process manually. You have sub
processes, branching and looping available:

.. code:: python

    import adhesive
    import uuid

    @adhesive.task("Run in parallel item {loop.value}")
    def context_to_run(context):
        if not context.data.executions:
            context.data.executions = set()

        context.data.executions.add(str(uuid.uuid4()))

    data = adhesive.process_start()\
        .branch_start()\
            .sub_process_start() \
                .task("Run in parallel",
                      loop="items") \
            .sub_process_end()\
        .branch_end() \
        .branch_start() \
            .sub_process_start() \
                .task("Run in parallel item {loop.value}",
                      loop="items") \
            .sub_process_end() \
        .branch_end() \
        .process_end()\
        .build(initial_data={"items": [1, 2, 3, 4, 5]})

    assert len(data.executions) == 10

Here you see the full BPMN power starting to unfold. We create a process
that branches out, creates sub processes (sub processes can be looped as
a single unit). Loops are creating execution tokens that also run in
parallel in the same pool.

Note that you can pass ``initial_data`` into the process, and you can
also get the ``context.data`` from the last execution token.

BPMN Process
------------

Last but not least, adhesive reads BPMN files, and builds the process
graph from them. This is particularly good if the process is complex and
has a lot of dependencies:

|BPMN Editor|

The `build of adhesive`_ is modeled as a `BPMN process`_ itself, so we
load it from the file directly using:
``adhesive.build_bpmn("adhesive-self.bpmn")``

.. code:: python

    import adhesive

    @adhesive.task("Read Parameters")
    def read_parameters(context) -> None:
        context.data.run_mypy = False
        context.data.test_integration = True

    @adhesive.task(re=r"^Ensure Tooling:\s+(.+)$")
    def gbs_ensure_tooling(context, tool_name) -> None:
        ge_tooling.ensure_tooling(context, tool_name)

    # ...

    adhesive.build_bpmn("adhesive-self.bpmn")

As you see steps are parametrizable, and use the data from the task name
into the step definition.

Defining BPMN Tasks
===================

For example here, we define an implementation of tasks using regex
matching, and extracting values:

.. code:: python

    @adhesive.task(re=r"^Ensure Tooling:\s+(.+)$")
    def gbs_ensure_tooling(context, tool_name) -> None:
        # ...

Or a user task (interactive form):

.. code:: python

    @adhesive.usertask('Publish to PyPI?')
    def publish_to_pypi_confirm(context, ui):
        ui.add_checkbox_group(
            "publish",
            title="Publish",
            values=(
                ("nexus", "Publish to Nexus"),
                ("pypitest", "Publish to PyPI Test"),
                ("pypi", "Publish to PyPI"),
            ),
            value=("pypitest", "pypi")
        )

Don’t forget, the ``@adhesive.task`` and ``@adhesive.usertask`` are just
defining mappings for implementations of the task names available in the
process. Only the ``adhesive.build()`` creates a linear process out of
the declaration of the tasks.

As you notice, there’s always a first parameter named ``context``. The
``context`` parameter contains the following information:

1. ``task`` - the Task in the graph that’s currently matched against
   this execution.

2. ``task_name`` - The resolved name, with the variables interpolated.
   Matching is attempted *after* the name is resolved.

3. ``data`` - Data that the current execution token contains. This data
   is always cloned across executions, and \`set\`s and \`dict\`s are
   automatically merged if multiple execution tokens are merged. So you
   have a modifiable copy of the data that you’re allowed to change, and
   is propagated into the following execution tokens.

4. ``loop`` - if the current task is in a loop, the entry contains its
   ``index``, the ``key`` and ``value`` of the items that are iterating,
   and the ``expression`` that was evaluated. Note that loop execution
   happens in parallel since these are simple execution tokens.

5. ``lane`` - the current lane where the tasks belongs. Implicitly it’s
   ``default``.

6. ``workspace`` - a way to interact with a system, and execute
   commands, create files, etc.

``adhesive`` runs all the tasks on a parallel process pool for better
performance. This happens automatically.

The tasks perform the actual work for the build. But in order to have
that, we need to be able to execute commands, and create files. For that
we have the ``workspace``.

Start Event Messages
====================

Adhesive supports also start events with messages in the process. Each
message start event, is being processed in its own thread and ``yield``
results:

.. code:: python

    @adhesive.message('Generate Event')
    def message_generate_event(context):
        for i in range(10):
            yield i

    @adhesive.task('Process Event')
    def process_event(context):
        print(f"event data: {context.data.event}")

Each yield generates a new event that fires up the connected tasks. The
data yielded is present in the ``event`` attribute in the token, for the
following tasks.

Callback Messages
-----------------

The other option to push messages into a process is to use callback
messages:

.. code:: python

    @adhesive.message_callback('REST: /rest/process-resource')
    def message_rest_rest_process_resource(context, callback):
        @app.route("/rest/resource/create")
        def create_resource():
            callback(Dict({
                "type": "CREATE"
            }))

            return "Create event fired"

Using this we’re able to hook into other systems that have their own
loop, such as in this case the Flask server, and push messages using the
``callback``. This approach has also the advantage of not creating new
threads for each message endpoint.

Connections
===========

Tasks are linked using connections. In some cases, connections can have
conditions. Conditions are expressions that when evaluated to ``True``
will allow the token to pass the connection. In the connection there is
access to the ``task``, ``task_name``, ``data``, ``loop``, ``lane`` and
``context``, as well as the variables defined in the ``context.data``.

So if in a task there is defined a data field such as:

.. code:: py

    @adhesive.task('prepare data')
    def prepare_data(context):
        context.data.navigation_direction = "forward"

The ``navigation_direction`` can be validated in the condition with any
of the following:

-  ``context.data.navigation_direction == "forward"``

-  ``data.navigation_direction == "forward"``

-  ``navigation_direction == "forward"``

Workspace
=========

Workspaces are just a way of interacting with a system, running
commands, and writing/reading files. Currently there’s support for:

-  the local system

-  docker containers

-  kubernetes

-  remote SSH connections

When starting ``adhesive`` allocates a default workspace folder in the
configured temp location (implicitly ``/tmp/adhesive``). The
``Workspace`` API is an API that allows you to run commands, and create
files, taking care of redirecting outputs, and even escaping the
commands to be able to easily run them inside docker containers.

The workspace is available from the cotext directly from the
``context``, by calling ``context.workspace``.

For example calling ``context.workspace.run(…​)`` will run the command
on the host where adhesive is running:

.. code:: python

    @adhesive.task("Run Maven")
    def build_project(context) -> None:
        context.workspace.run("mvn clean install")

If we’re interested in the program output we simply do a ``run`` with a
``capture_stdout`` that returns the output as a string:

.. code:: python

    @adhesive.task("Test")
    def gbs_test_linux(context) -> None:
        content = context.workspace.run("echo yay", capture_stdout=True)
        assert content == "yay"

or we can use the simplified call with ``run_output`` that guarantees a
``str`` as result, unlike the ``Optional[str]`` for ``run``:

.. code:: python

    @adhesive.task("Test")
    def gbs_test_linux(context) -> None:
        content = context.workspace.run_output("echo yay")
        assert content == "yay"

The ``run`` commands implicitly use ``/bin/sh``, but a custom shell can
be specified by passing the ``shell`` argument:

.. code:: python

    content = context.workspace.run_output("echo yay", shell="/bin/bash")

Docker Workspace
----------------

To create a docker workspace that runs inside a container with the
tooling you just need to:

.. code:: python

    from adhesive.workspace import docker

Then to spin up a container that has the current folder mounted in,
where you’re able to execute commands *inside* the container. You just
need to:

.. code:: python

    @adhesive.task("Test")
    def gbs_test_linux(context) -> None:
        image_name = 'some-custom-python'

        with docker.inside(context.workspace, image_name) as w:
            w.run("python -m pytest -n 4")

This creates a container using our current context workspace, where we
simply execute what we want, using the ``run()`` method. After the
``with`` statement the container will be teared down automatically.

SSH Workspace
-------------

In order to have ssh, make sure you installed ``adhesive`` with SSH
support:

.. code:: sh

    pip install -U adhesive[ssh]

To have a SSH Workspace, it’s again the same approach:

.. code:: python

    from adhesive.workspace import ssh

Then to connect to a host, you can just use the ``ssh.inside`` the same
way like in the docker sample:

.. code:: python

    @adhesive.task("Run over SSH")
    def run_over_ssh(context) -> None:
        with ssh.inside(context.workspace,
                        "192.168.0.51",
                        username="raptor",
                        key_fileaname="/home/raptor/.ssh/id_rsa") as s:
            s.run("python -m pytest -n 4")

The parameters are being passed to paramiko, that’s the implementation
beneath the ``SshWorkspace``.

Kubernetes Workspace
--------------------

To run things in pods, it’s the same approach:

.. code:: python

    from adhesive.workspace import kube

Then we can create a workspace to run things in kubernetes pods. The
workspace, as well as the API, will use the ``kubectl`` command
internally.

.. code:: python

    @adhesive.task("Run things in the pod")
    def run_in_the_pod(context) -> None:
        with kube.inside(context.workspace,
                         pod_name="nginx-container") as pod:
            pod.run("ps x")  # This runs in the pod

Kubernetes API
--------------

Adhesive also packs a kubernetes api, that’s available on the
``adhesive.kubeapi``:

.. code:: python

    from adhesive.kubeapi import KubeApi

To use it, we need to create an instance against a workspace.

.. code:: python

    @adhesive.gateway('Determine action')
    def determine_action(context):
        kubeapi = KubeApi(context.workspace,
                          namespace=context.data.target_namespace)

Let’s create a namespace:

.. code:: python

    kubeapi.create(kind="ns", name=context.data.target_namespace)

Or let’s create a service using the ``kubectl apply`` approach:

.. code:: python

        kubeapi.apply(f"""
            apiVersion: v1
            kind: Service
            metadata:
                name: nginx-http
                labels:
                    app: {context.data.target_namespace}
            spec:
                type: ClusterIP
                ports:
                - port: 80
                  protocol: TCP
                  name: http
                selector:
                  app: {context.data.target_namespace}
        """)

Or let’s get some pods:

.. code:: python

        pod_definitions = kubeapi.getall(
            kind="pod",
            filter=f"execution_id={context.execution_id}",
            namespace=context.data.target_namespace)

These returns objects that allow navigating properties as regular python
attributes:

.. code:: python

        new_pods = dict()
        for pod in pod_definitions:
            if not pod.metadata.name:
                raise Exception(f"Wrong definition {pod}")

            new_pods[pod.metadata.name] = pod.status.phase

You can also navigate properties that are not existing yet, for example
to wait for the status of a pod to appear:

.. code:: python

    @adhesive.task('Wait For Pod Creation {loop.key}')
    def wait_for_pod_creation_loop_value_(context):
        kubeapi = KubeApi(context.workspace,
                          namespace=context.data.target_namespace)
        pod_name = context.loop.key
        pod_status = context.loop.value

        while pod_status != 'Running':
            time.sleep(5)
            pod = kubeapi.get(kind="pod", name=pod_name)

            pod_status = pod.status.phase

To get the actual data from the wrappers that the adhesive API creates,
you can simply call the ``_raw`` property.

Workspace API
-------------

Here’s the full API for it:

.. code:: python

    class Workspace(ABC):
        """
        A workspace is a place where work can be done. That means a writable
        folder is being allocated, that might be cleaned up at the end of the
        execution.
        """

        @abstractmethod
        def write_file(
                self,
                file_name: str,
                content: str) -> None:
            pass

        @abstractmethod
        def run(self,
                command: str,
                capture_stdout: bool = False) -> Union[str, None]:
            """
            Run a new command in the current workspace.

            :param capture_stdout:
            :param command:
            :return:
            """
            pass

        @abstractmethod
        def rm(self, path: Optional[str]=None) -> None:
            """
            Recursively remove the file or folder given as path. If no path is sent,
            the whole workspace will be cleared.

            :param path:
            :return:
            """
            pass

        @abstractmethod
        def mkdir(self, path: str=None) -> None:
            """
            Create a folder, including all its needed parents.

            :param path:
            :return:
            """
            pass

        @abstractmethod
        def copy_to_agent(self,
                          from_path: str,
                          to_path: str) -> None:
            """
            Copy the files to the agent from the current disk.
            :param from_path:
            :param to_path:
            :return:
            """
            pass

        @abstractmethod
        def copy_from_agent(self,
                            from_path: str,
                            to_path: str) -> None:
            """
            Copy the files from the agent to the current disk.
            :param from_path:
            :param to_path:
            :return:
            """
            pass

        @contextmanager
        def temp_folder(self):
            """
            Create a temporary folder in the current `pwd` that will be deleted
            when the `with` block ends.

            :return:
            """
            pass

        @contextmanager
        def chdir(self, target_folder: str):
            """
            Temporarily change a folder, that will go back to the original `pwd`
            when the `with` block ends. To change the folder for the workspace
            permanently, simply assing the `pwd`.
            :param target_folder:
            :return:
            """
            pass

User Tasks
==========

In order to create user interactions, you have user tasks. These define
form elements that are populated in the ``context.data``, and available
in subsequent tasks.

When a user task is encountered in the process flow, the user is
prompted to fill in the parameters. Note that the other started tasks
continue running, proceeding forward with the build.

The ``name`` used in the method call defines the name of the variable
that’s in the ``context.data``.

For example in here we define a checkbox group that allows us to pick
where to publish the package:

.. code:: python

    @adhesive.usertask("Read User Data")
    def read_user_data(context, ui) -> None:
        ui.add_input_text("user",
                title="Login",
                value="root")
        ui.add_input_password("password",
                title="Password")
        ui.add_checkbox_group("roles",
                title="Roles",
                value=["cyborg"],
                values=["admin", "cyborg", "anonymous"])
        ui.add_radio_group("disabled",  # title is optional
                values=["yes", "no"],
                value="no")
        ui.add_combobox("machine",
                title="Machine",
                values=(("any", "<any>"),
                        ("win", "Windows"),
                        ("lin", "Linux")))

This will prompt the user with this form:

|form|

This data is also available for edge conditions, so in the BPMN modeler
we can define a condition such as ``"pypi" in context.data.roles``, or
since ``data`` is also available in the edge scope:
``"pypi" in data.roles``.

The other option is simply reading what the user has selected in a
following task:

.. code:: python

    @adhesive.task("Register User")
    def publish_items(context):
        for role in context.data.roles:
            # ...

User tasks support the following API, available on the ``ui`` parameter,
the parameter after the context:

.. code:: python

    class UiBuilderApi(ABC):
        def add_input_text(self,
                           name: str,
                           title: Optional[str] = None,
                           value: str = '') -> None:

        def add_input_password(self,
                               name: str,
                               title: Optional[str] = None,
                               value: str = '') -> None:

        def add_combobox(self,
                         name: str,
                         title: Optional[str] = None,
                         value: Optional[str]=None,
                         values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:

        def add_checkbox_group(
                self,
                name: str,
                title: Optional[str]=None,
                value: Optional[Iterable[str]]=None,
                values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:

        def add_radio_group(self,
                            name: str,
                            title: Optional[str]=None,
                            value: Optional[str]=None,
                            values: Optional[List[Any]]=None) -> None:

        def add_default_button(self,
                               name: str,
                               title: Optional[str] = None,
                               value: Optional[Any] = True) -> None:

Custom Buttons
--------------

In order to allow navigation inside the process, the
``add_default_button`` API exists to permit creation of buttons.
Implicitly a single button with an ``OK`` label is added to the User
Task, that when pressed fills the ``context.data`` in the outgoing
execution token.

With ``add_default_button`` we create custom buttons such as ``Back``
and ``Forward``, or whatever we need in our process. Unlike the default
``OK`` button, when these are called, they also set in the
``context.data`` the ``value`` that’s assigned to them. This value we
use then further in a ``Gateway``, or simple as a condition on the
outgoing edges.

The title is optional, and only if missing it’s build either from the
``name`` if all the buttons in the form have unique names, since they
assign a different variable in the ``context.data``, or from the
``value`` if they have overlapping names.

Secrets
=======

Secrets are files that contain sensitive information are not checked in
the project. In order to make them available to the build, we need to
define them in either ``~/.adhesive/secrets/SECRET_NAME`` or in the
current folder as ``.adhesive/secrets/SECRET_NAME``.

In order to make them available, we just use the ``secret`` function
that creates the file in the current workspace and deletes it when
exiting. For example here’s how we’re doing the actual publish, creating
the secret inside a docker container:

.. code:: python

    @adhesive.task('^PyPI publish to (.+?)$')
    def publish_to_pypi(context, registry):
        with docker.inside(context.workspace, context.data.gbs_build_image_name) as w:
            with secret(w, "PYPIRC_RELEASE_FILE", "/germanium/.pypirc"):
                w.run(f"python setup.py bdist_wheel upload -r {registry}")

Note the ``docker.inside`` that creates a different workspace.

Configuration
=============

Adhesive supports configuration via its config files, or environment
variables. The values are read in the following order:

1. environment variables: ``ADHESIVE_XYZ``, then

2. values that are in the project config yml file:
   ``.adhesive/config.yml``, then

3. values configured in the global config yml file:
   ``$HOME/.adhesive/config.yml``.

Currently the following values are defined for configuration:

temp\_folder
------------

default value ``/tmp/adhesive``, environment var:
``ADHESIVE_TEMP_FOLDER``.

Is where all the build files will be stored.

plugins
-------

default value ``[]``, environment var: ``ADHESIVE_PLUGINS_LIST``.

This contains a list of folders, that will be added to the ``sys.path``.
So to create a reusable plugin that will be reused by multiple builds,
you need to simply create a folder with python files, then point to it
in the ``~/.adhesive/config.yml``:

.. code:: yaml

    plugins:
    - /path/to/folder

Then in the python path you can simply do regular imports.

color
-----

default value ``True``, environment var: ``ADHESIVE_COLOR``.

Marks if the logging should use ANSI colors in the terminal. Implicitly
this is ``true``, but if log parsing is needed, it can make sense to
have it false.

log\_level
----------

default\_value ``info``, environment var: ``ADHESIVE_LOG_LEVEL``.

How verbose should the logging be on the terminal. Possible values are
``trace``, ``debug``, ``info``, ``warning``, ``error`` and ``critical``.

pool\_size
----------

default value is empty, environment var: ``ADHESIVE_POOL_SIZE``.

Sets the number of workers that adhesive will use. Defaults to the
number of CPUs if unset.

stdout
------

default value is empty, environment var: ``ADHESIVE_STDOUT``.

Implicitly for each task, the log is redirected in a different file, and
only shown if the task failed. The redirection can be disabled.

parallel\_processing
--------------------

default value is ``thread``, environment var:
``ADHESIVE_PARALLEL_PROCESSING``.

Implicitly tasks are scaled using multiple threads in order to alleviate
waits for I/O. This is useful for times when remote ssh workspaces are
defined in the lanes, so the same connection can be reused for multiple
tasks.

This value can be set to ``process``, in case the tasks are CPU
intensive. This has the drawback of recreating the connections on
workspaces' each task execution.

Hacking Adhesive
================

Adhesive builds with itself. In order to do that, you need to checkout
the `adhesive-lib`_ shared plugin, and configure your local config to
use it:

.. code:: yaml

    plugins:
    - /path/to/adhesive-lib

Then simply run the build using adhesive itself:

.. code:: sh

    adhesive

.. _build of adhesive: _adhesive.py
.. _BPMN process: adhesive-self.bpmn
.. _adhesive-lib: https://github.com/germaniumhq/adhesive-lib

.. |BPMN Editor| image:: ./doc/yaoqiang-screenshot.png
.. |form| image:: ./doc/console_usertask.png

