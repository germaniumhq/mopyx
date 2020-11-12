import adhesive
import unittest

test = unittest.TestCase()


@adhesive.message('Generate Events')
def message_generate_events(context: adhesive.Token):
    message_ids = ["a", "a", "b", "a", "a", "a", "a", "b"]
    for i in range(len(message_ids)):
        yield {
            "id": message_ids[i],
            "event_index": str(i),
        }


@adhesive.task('Event Check {event.id}')
def event_check(context: adhesive.Token) -> None:
    pass


@adhesive.task('Event Execute {event.id}', deduplicate="event.id")
def event_execute(context: adhesive.Token) -> None:
    context.data.executed = { context.data.event["id"] }


data = adhesive.bpmn_build(
    "deduplicate-multiple-bug.bpmn",
    wait_tasks=False,
)
test.assertEqual({"a", "b"}, data.executed)
