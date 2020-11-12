import adhesive
import unittest
import uuid

test = unittest.TestCase()


@adhesive.task('First task')
def first_task(context):
    context.data.first_task.add(str(uuid.uuid4()))


@adhesive.task('Second task')
def second_task(context):
    context.data.second_task.add(str(uuid.uuid4()))


@adhesive.task('Third task')
def third_task(context):
    context.data.third_task.add(str(uuid.uuid4()))


@adhesive.task('Fourth task')
def fourth_task(context):
    context.data.fourth_task.add(str(uuid.uuid4()))


# we run it with wait_tasks = false because we want to ensure we have only one
# connection happening.
data = adhesive.process_start()\
    .task('First task')\
    .task('Second task', when="data.not_skip")\
    .task('Second task', when="data.not_skip")\
    .task('Third task', when="data")\
    .task('Third task', when="data")\
    .task('Fourth task')\
    .process_end()\
    .build(initial_data={
        "first_task": set(),
        "second_task": set(),
        "third_task": set(),
        "fourth_task": set(),
    })

test.assertEqual(1, len(data.first_task), "Expected a single first task execution")
test.assertEqual(0, len(data.second_task), "Expected no second task executions")
test.assertEqual(2, len(data.third_task), "Expected a double third task execution")
test.assertEqual(1, len(data.fourth_task), "Expected a single fourth task execution")
