import uuid
import adhesive


@adhesive.task("Basic loop", loop="data.loop_items")
def basic_loop(context):
    if not context.data.executions:
        context.data.executions = set()

    context.data.executions.add(str(uuid.uuid4()))


@adhesive.task("Not a loop")
def not_a_loop(context):
    if not context.data.executions:
        context.data.executions = set()

    context.data.executions.add(str(uuid.uuid4()))


result = adhesive.build(initial_data={
    "loop_items": []
})

# the task after the loop should still execute
assert len(result.executions) == 1
