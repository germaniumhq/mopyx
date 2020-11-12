import adhesive
import uuid
import time
import unittest


test = unittest.TestCase()


@adhesive.task('Sleep 3 Seconds')
def sleep_2_seconds(context):
    time.sleep(2.5)


@adhesive.task('Timeout was Called')
def timeout_was_called(context):
    context.data.timeout_was_called = {uuid.uuid4()}


data = adhesive.bpmn_build(
    "one-second-timer.bpmn",
    wait_tasks=False)

test.assertTrue(data.timeout_was_called, "Timer was not called :(")
test.assertEqual(2, len(data.timeout_was_called), "The cycle timer should be called twice")
