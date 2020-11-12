import random
import unittest
import uuid
from typing import Dict, Set, Any

import adhesive

test = unittest.TestCase()

already_running: Set[str] = set()
pending_events: Dict[str, Any] = dict()


def get_event_id(event) -> str:
    return event["event_id"]


@adhesive.message('Start Event')
def message_start_event(context):
	# generate 100 events really fast
    for i in range(100):
        yield {
            "index": i,
            "state": "new",
            "event_id": str(random.randint(0,2))
        }


@adhesive.gateway('Deduplicate Events')
def deduplicate_events(context):
    global already_running
    global pending_events

    event = context.data.event
    event_id = get_event_id(event)

    context.data.event_id = event_id

    # Since we already have events running, we let this token
    # pass through. Since the state will be "new" and not "process"
    # we'll drop this token.
    if context.data.event["state"] == "new" and event_id in already_running:
        pending_events[event_id] = event
        return context.data

    # If we're getting notified that a task finished, we're marking
    # the task as not running anymore for that event id type
    if context.data.event["state"] == "done":
        already_running.remove(event_id)

    # If we did a loop and we returned with the done event, and nothing
    # else is waiting we return
    if context.data.event["state"] == "done" and event_id not in pending_events:
        return context.data

    # we have either a new event, or a done event arriving
    if context.data.event["state"] == "done":
        context.data.event = pending_events[event_id]
        del pending_events[event_id]

    context.data.event["state"] = "process"
    already_running.add(event_id)

    return context.data


@adhesive.task("Execute Task for {event_id}")
def execute_task(context):
    context.data.executed_tasks.add(str(uuid.uuid4()))


@adhesive.task('Set the event as processed')
def set_the_event_as_processed(context):
    context.data.event["state"] = "done"


data = adhesive.bpmn_build("deduplicate.bpmn",
    wait_tasks=False,
    initial_data={
        "executed_tasks": set(),
    })


# most events should be deduplicated
test.assertTrue(len(data.executed_tasks) < 20)
