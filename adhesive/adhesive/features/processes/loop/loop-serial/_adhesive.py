import adhesive
import unittest

test = unittest.TestCase()


@adhesive.task('Run Task serially')
def run_task_in_loop(context):
    context.data.count += context.loop.index


result = adhesive.bpmn_build("loop-serial.bpmn",
    initial_data={
        "items": ["1", "2", "3"],
        "count": 1,
    })

# execution is serial, so the value is:
# 1 + 0, then 1 + 1, then 2 + 2 == 4
print(f"result count was {result.count}")
test.assertEqual(4, result.count, "Loop execution was probably not serial")

