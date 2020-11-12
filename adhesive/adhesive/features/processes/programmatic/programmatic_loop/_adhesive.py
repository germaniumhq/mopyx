import adhesive
import uuid


@adhesive.task("Run in parallel")
def context_to_run(context):
    if not context.data.executions:
        context.data.executions = set()

    context.data.executions.add(str(uuid.uuid4()))


data = adhesive.process_start()\
    .branch_start()\
        .subprocess_start() \
            .task("Run in parallel",
                  loop="context.data.items") \
        .subprocess_end()\
    .branch_end() \
    .branch_start() \
        .subprocess_start() \
            .task("Run in parallel",
                  loop="context.data.items") \
        .subprocess_end() \
    .branch_end() \
    .process_end()\
    .build(initial_data={"items": [1, 2, 3, 4, 5]})


assert len(data.executions) == 10
