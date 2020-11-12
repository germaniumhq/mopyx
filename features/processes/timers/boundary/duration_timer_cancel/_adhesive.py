import adhesive
import time
import unittest


test = unittest.TestCase()


@adhesive.task('Sleep 2 Seconds')
def sleep_2_seconds(context):
    time.sleep(2)


@adhesive.task('Timeout was Called')
def timeout_was_called(context):
    context.data.timeout_was_called = True


data = adhesive.bpmn_build(
    "one-second-timeout.bpmn",
    wait_tasks=False)

test.assertTrue(data.timeout_was_called, "Timeout was not called :(")
