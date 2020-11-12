import adhesive
import uuid
import unittest

test = unittest.TestCase()


@adhesive.task('Running {loop.value} on {loop.parent_loop.value}')
def run_simple_task(context):
    print(f"{context.task_name}")
    context.data.execution_count.add(str(uuid.uuid4()))


data = adhesive.process_start()\
    .subprocess_start("Run builds on {loop.value}", loop="platforms")\
        .task("Running {loop.value} on {loop.parent_loop.value}", loop="tasks")\
    .subprocess_end()\
    .build(initial_data={
        "execution_count": set(),
        "platforms": ["linux", "windows", "solaris"],
        "tasks": ["archive", "compute", "list"],
    })

test.assertEqual(9, len(data.execution_count))
