import adhesive
import uuid
import unittest

test = unittest.TestCase()


@adhesive.task('Raise Error {loop.index}')
def raise_error_loop_index_(context: adhesive.Token) -> None:
    raise Exception(f"error for {context.loop.index}")


@adhesive.task('Error Caught')
def error_caught(context: adhesive.Token) -> None:
    context.data.errors_caught = { str(uuid.uuid4()) }


@adhesive.task('Should Not Be Reachable')
def should_not_be_reachable(context: adhesive.Token) -> None:
    raise Exception("Should not be reachable")


data = adhesive.bpmn_build(
    "loop_exceptions.bpmn",
    wait_tasks = False,
    initial_data = {
        "items": range(20),
    }
)

test.assertTrue(data.errors_caught)
test.assertEqual(1, len(data.errors_caught))

