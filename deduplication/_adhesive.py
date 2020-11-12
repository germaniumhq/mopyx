from typing import Dict, Set, Any

import adhesive
import uuid
import unittest
import random
import threading


test = unittest.TestCase()

@adhesive.message('Start Event')
def message_start_event(context):
    # generate 100 events really fast
    for i in range(10000):
        yield {
            "index": i,
            "state": "new",
            "event_id": str(random.randint(0, 2))
        }


@adhesive.task("Execute Task for {event.event_id}",
               deduplicate="event.event_id")
def execute_task(context):
    context.data.executed_tasks.add(str(uuid.uuid4()))


data = adhesive.bpmn_build("deduplicate.bpmn",
    wait_tasks=False,
    initial_data={
        "executed_tasks": set(),
    })


# most events should be deduplicated
test.assertTrue(len(data.executed_tasks) < 10)

