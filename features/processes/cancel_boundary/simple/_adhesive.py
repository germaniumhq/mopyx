import adhesive
import unittest

test = unittest.TestCase()

@adhesive.task('Sleep 2 Seconds')
def sleep_2_seconds(context: adhesive.Token) -> None:
    context.workspace.run("""
        sleep 2
    """)


@adhesive.task('Timeout Happened')
def timeout_happened(context: adhesive.Token) -> None:
    context.data.timeout_happened = True


@adhesive.task('Should Not Execute')
def should_not_execute(context: adhesive.Token) -> None:
    raise Exception("Should not be called")


@adhesive.task('Error Happened')
def error_happened(context: adhesive.Token) -> None:
    context.data.error_happened = True
    context.data._error = None


data = adhesive.bpmn_build("cancel-boundary.bpmn")

test.assertTrue(data.timeout_happened)
test.assertFalse(data.error_happened, "The error boundary event was triggered on timeout")
test.assertFalse(data._error, "An exception happened in the process")

