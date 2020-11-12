import adhesive
from adhesive.workspace import noop
import unittest
import uuid


test = unittest.TestCase()


@adhesive.lane('custom')
def lane_custom(context):
    with noop.inside(context.workspace) as w:
        context.data.lane_executions.add(str(uuid.uuid4()))
        yield w


@adhesive.task('Task', lane="custom", loop="items")
def simple_task(context):
    context.data.task_executions.add(str(uuid.uuid4()))
    test.assertTrue(
            isinstance(context.workspace, noop.NoopWorkspace),
            "The workspace should be the workspace from the lane")


data = adhesive.build(initial_data={
        "items": range(3),
        "task_executions": set(),
        "lane_executions": set(),
    })


test.assertEqual(1, len(data.lane_executions), "The lane should have only executed once")
test.assertEqual(3, len(data.task_executions), "The tasks should have executed three times")

