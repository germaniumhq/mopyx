import adhesive
from adhesive.workspace import noop

import uuid
import unittest

test = unittest.TestCase()


@adhesive.lane('custom')
def lane_custom(context):
    with noop.inside(context.workspace) as w:
        context.data.lane_executions.add(str(uuid.uuid4()))
        yield w


@adhesive.task(re='Running (.*) on (.*)')
def run_simple_task(context, task_name, platform):
    print(f"Running {task_name} on {platform}")

    test.assertTrue(
            isinstance(context.workspace, noop.NoopWorkspace),
            "The workspace from the lane was not present")

    context.data.task_executions.add(str(uuid.uuid4()))


data = adhesive.process_start()\
    .subprocess_start("Run builds on {loop.value}", loop="platforms", lane="custom")\
        .task("Running {loop.value} on {loop.parent_loop.value}", loop="tasks", lane="custom")\
    .subprocess_end()\
    .build(initial_data={
        "task_executions": set(),
        "lane_executions": set(),
        "platforms": ["linux", "windows", "mac"],
        "tasks": ["archive", "untar", "backup"],
    })


test.assertEqual(9, len(data.task_executions))
test.assertEqual(1, len(data.lane_executions))
