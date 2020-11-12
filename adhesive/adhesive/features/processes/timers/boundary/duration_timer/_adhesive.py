import adhesive
import time
import uuid
import unittest


test = unittest.TestCase()


@adhesive.task('Sleep 2 Seconds')
def sleep_2_seconds(context):
    time.sleep(2)


@adhesive.task('Timeout was Called')
def timeout_was_called(context):
    context.data.timeout_was_called = {uuid.uuid4()}


data = adhesive.bpmn_build(
    "one-second-timeout.bpmn",
    wait_tasks=False)

test.assertTrue(data.timeout_was_called, "Timeout was not called :(")
test.assertEqual(1, len(data.timeout_was_called), "The timeout should be called only once")
