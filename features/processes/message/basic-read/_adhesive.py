import adhesive
import uuid
import unittest
import logging
import time

LOG = logging.getLogger(__name__)

test = unittest.TestCase()


@adhesive.message('Generate Event')
def message_generate_event(context):
    for i in range(5):
        yield i
        time.sleep(0.2)  # we give it time so the process can exit


@adhesive.task('Process Event')
def process_event(context):
    context.data.executions = set()
    context.data.executions.add(str(uuid.uuid4()))

    LOG.info(f"event data: {context.data.event}")


data = adhesive.bpmn_build("basic-read.bpmn",
                            wait_tasks=False)


test.assertEqual(5, len(data.executions))
