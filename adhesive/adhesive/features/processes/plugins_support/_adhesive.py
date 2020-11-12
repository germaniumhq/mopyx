from some_plugin import set_x_into_context_data
import adhesive


@adhesive.task("set x")
def set_x_from_plugin(context):
    set_x_into_context_data(context)


@adhesive.task("check x")
def check_x(context):
    assert context.data.x == 1


adhesive.build()
