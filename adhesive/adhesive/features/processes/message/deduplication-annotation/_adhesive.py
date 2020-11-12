import time
import unittest
import uuid

import adhesive

test = unittest.TestCase()

already_running = False
pending_events = False


@adhesive.message('Start Event')
def message_start_event(context):
    # generate 100 events really fast
    for i in range(50):
        yield {
            "index": i,
            "id": "new" + str(i % 8),
        }

    time.sleep(2)

    for i in range(50):
        yield {
            "index": i,
            "id": "new" + str(i % 8),
        }


@adhesive.task('Deduplicate Task',
               deduplicate="event.id")
def deduplicate_task(context):
    context.data.extra_id = context.data.event["id"]


@adhesive.task('Execute Task')
def execute_task(context):
    time.sleep(0.2)
    context.data.executed_tasks.add(str(uuid.uuid4()))

    test.assertEqual(context.data.extra_id, context.data.event["id"])


@adhesive.task('Noop')
def noop(context: adhesive.Token) -> None:
    pass


@adhesive.task('Noop2')
def noop2(context: adhesive.Token) -> None:
    pass


data = adhesive.bpmn_build("deduplicate.bpmn",
    wait_tasks=False,
    initial_data={
        "executed_tasks": set(),
    })

test.assertEqual(32, len(data.executed_tasks))
