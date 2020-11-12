import adhesive
import uuid


@adhesive.task("Basic loop", loop="data.loop_items")
def basic_loop(context):
    if not context.data.executions:
        context.data.executions = set()

    context.data.executions.add(str(uuid.uuid4()))


result = adhesive.build(initial_data={
    "loop_items": [1, 2, 3, 4, 5]
})

assert len(result.executions) == 5
