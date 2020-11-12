import time
import adhesive
import uuid
import unittest

test = unittest.TestCase()


@adhesive.message('Generate Events')
def message_generate_events(context: adhesive.Token):
    for i in range(4):
        time.sleep(0.3)
        yield {
            "id": "abc",
            "index": i,
        }


@adhesive.task('Deduplicate event on id', deduplicate="event.id")
def deduplicate_event_on_id(context: adhesive.Token) -> None:
    pass


@adhesive.task('Task')
def task(context: adhesive.Token) -> None:
    time.sleep(1)
    context.data.executions = { str(uuid.uuid4()) }


data = adhesive.bpmn_build("downstream-calls.bpmn", wait_tasks=False)

test.assertEqual(2, len(data.executions))

