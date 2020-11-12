import adhesive
from adhesive.workspace import noop
import unittest


test = unittest.TestCase()


@adhesive.lane('custom')
def lane_custom(context):
    with noop.inside(context.workspace) as w:
        yield w


@adhesive.task('Task')
def simple_task(context):
    test.assertTrue(isinstance(context.workspace, noop.NoopWorkspace))


adhesive.process_start()\
    .task("Task", lane="custom")\
    .process_end()\
    .build()
