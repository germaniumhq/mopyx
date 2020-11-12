import adhesive
import unittest

test = unittest.TestCase()


@adhesive.task('Task')
def task(context):
    context.data.execution_count += 1
    context.data.parallel_check += context.loop.index

    if context.loop.index >= 2:
        context.data.loop_condition = False


data = adhesive.bpmn_build("loop-parallel-condition.bpmn",
    initial_data={
        "loop_condition": True,
        "execution_count": 0,
        "parallel_check": 1,
    })

test.assertEqual(3, data.execution_count)
# 5 == 1 (initial value) + 0 + 1 + 2
test.assertEqual(4, data.parallel_check,
                 "The loop probably didn't executed serially")

