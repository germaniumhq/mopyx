import adhesive
import time
import uuid

import unittest

from adhesive.execution.ExecutionToken import ExecutionToken
from adhesive import WorkspaceGenerator

test = unittest.TestCase()


@adhesive.lane(re="docker: (.*)")
def docker_lane(context, image_name) -> WorkspaceGenerator:
    if not context.workspace:
        raise Exception("No workspace is defined.")

    result = context.workspace.clone()

    yield result


@adhesive.task(
    'Ensure Docker Tooling',
    'Test Chrome',
    'Test Firefox',
    'Build Germanium Image',
    'Build Germanium Image on {loop.value}',
    'Prepare Firefox',
    # exclusive gateway
    'Exclusive Task Branch',
    'Populate task data',
    'Exclusive default branch',
    'Cleanup Broken Tasks',
    'Error Was Caught',
    'Error Was Not Caught',
    re=[
        '^Cleanup Platform .*?$',
        '^Test Browser .*? on .*?$',
    ]
)
def basic_task(context) -> None:
    # small sanity check for loops. If we have a loop on the task in the graph,
    # we must also have a loop in the token.
    if context.task.loop:
        test.assertTrue(context.loop.expression)
        test.assertEqual(context.loop.expression, context.task.loop.loop_expression)

    add_current_task(context)


@adhesive.task(re=r'^Parallel \d+$')
def parallel_task(context) -> None:
    time.sleep(1)
    if not context.data.executions:
        context.data.executions = set()

    context.data.executions.add(context.task_name)


@adhesive.task(
    'Throw Some Exception',
    'Throw Some Error',
)
def throw_some_exception(context) -> None:
    add_current_task(context)

    raise Exception("broken")


@adhesive.task('Increment X by 1')
def increment_x_by_1(context):
    add_current_task(context)

    if not context.data.x:
        context.data.x = 1
        return

    context.data.x += 1


@adhesive.task('Store current execution id')
def store_current_execution_id(context: ExecutionToken):
    add_current_task(context)
    context.data.execution_id = context.execution_id


@adhesive.task(re='^sh:(.*)$')
def execute_sh_command(context: adhesive.Token, command: str):
    add_current_task(context)
    context.workspace.run(command)


@adhesive.usertask('Read Data From User')
def read_data_from_user(context, ui) -> None:
    ui.add_input_text("branch", title="Branch")
    ui.add_input_password("password", title="Password")
    ui.add_combobox("version", title="Version", values=["12.0", "12.1", "12.2", "12.3"])
    ui.add_checkbox_group(
        "run_tests",
        title="Tests",
        value=("integration",),
        values=("integration", "Integration Tests"))
    ui.add_radio_group(
        "depman",
        title="Depman"
    )

    ui.add_default_button("OK")
    ui.add_default_button("Cancel")


@adhesive.gateway('Complex Gateway')
def complex_gateway(context) -> None:
    context.data.selected_browsers = {'firefox'}


def add_current_task(context):
    if not context.data.executions:
        context.data.executions = dict()

    if context.task_name not in context.data.executions:
        context.data.executions[context.task_name] = set()

    context.data.executions[context.task_name].add(str(uuid.uuid4()))
    print(context.task_name)
