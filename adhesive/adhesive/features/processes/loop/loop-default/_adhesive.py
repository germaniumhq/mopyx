import adhesive
import unittest

test = unittest.TestCase()


@adhesive.task('Run Task in loop')
def run_task_in_loop(context):
    context.data.count += context.loop.index


result = adhesive.bpmn_build("loop.bpmn",
    initial_data={
        "items": ["1", "2", "3"],
        "count": 1,
    })

# execution should happen in parallel, any of the cases, the value would
# be at most max index(2) + initial count(1) == 3
print(f"result count was {result.count}")
test.assertTrue(result.count <= 3, "Loop execution went terribly wrong")
test.assertTrue(result.count >= 1, "Loop execution went terribly wrong")
