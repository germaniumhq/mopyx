import adhesive
import time


@adhesive.message('Generate events')
def message_generate_events(context: adhesive.Token):
    for i in range(4):
        yield {
          "id": "a",
          "index": i,
        }
        time.sleep(1)


@adhesive.task('Deduplicate Task on {event.id}', deduplicate='event.id')
def deduplicate_task(context: adhesive.Token) -> None:
    time.sleep(2)


@adhesive.task('Fail first execution')
def fail_first_execution(context: adhesive.Token) -> None:
    if context.data.event["index"] == 0:
        raise Exception("task failed")


adhesive.bpmn_build("deduplicate_fail_downstream.bpmn", wait_tasks=False)
