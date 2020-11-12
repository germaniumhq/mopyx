import adhesive
import time


@adhesive.message('Generate events every hour')
def message_generate_events_every_hour(context: adhesive.Token):
    message_data = 'data'
    for i in range(2):
        yield message_data
        time.sleep(3600)


@adhesive.task('Fail the process')
def fail_the_process(context: adhesive.Token) -> None:
    raise Exception("fail the process")


adhesive.bpmn_build("event-failure.bpmn")

