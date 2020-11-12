import adhesive


@adhesive.task('put data in context')
def put_data_in_context(context):
    context.data.some_text = "Resolved Value"


@adhesive.task('read data {some_text}')
def print_data_from_context(context):
    pass


adhesive.build()
