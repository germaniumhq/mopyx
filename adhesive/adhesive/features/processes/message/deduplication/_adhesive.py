import adhesive
import addict
import time
import uuid
import unittest


test = unittest.TestCase()

already_running = False
pending_events = False

@adhesive.message('Start Event')
def message_start_event(context):
	# generate 100 events really fast
    for i in range(100):
        yield {
            "index": i,
            "state": "new",
        }


@adhesive.gateway('Deduplicate Events')
def deduplicate_events(context):
    global already_running
    global pending_events

    if context.data.event["state"] == "new" and already_running:
        pending_events = True
        return context.data  # We collapse the current event

    if context.data.event["state"] == "done":
        already_running = False

    if context.data.event["state"] == "done" and not pending_events:
        return context.data

    # we have either a new event, or a done event arriving
    context.data.event["state"] = "process"
    pending_events = False
    already_running = True

    return context.data


@adhesive.task('Execute Task')
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

