import adhesive


@adhesive.message('Generate Events')
def message_generate_events(context: adhesive.Token):
    yield {
        'id': 'Resolved Id',
        'data': 'Resolved Data',
    }


@adhesive.task('Event Check {event.id}')
def event_check_event_id_(context: adhesive.Token) -> None:
    pass


@adhesive.task('Event Execute {event.data}')
def event_execute_event_id_(context: adhesive.Token) -> None:
    pass


adhesive.bpmn_build("message-interpolation-events.bpmn")
