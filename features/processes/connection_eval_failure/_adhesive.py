import adhesive


@adhesive.task('Noop Task')
def noop_task(context):
    pass


@adhesive.task('Error Was Correctly Routed')
def error_was_routed(context):
    context.data.error_was_routed = True


data = adhesive.bpmn_build("test.bpmn")

assert data.error_was_routed

