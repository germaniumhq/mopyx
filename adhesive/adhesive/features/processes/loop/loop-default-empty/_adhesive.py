import adhesive


@adhesive.task('Loop on empty collection')
def loop_on_empty_collection(context):
    raise Exception("shold not execute")


@adhesive.task('Task after loop')
def task_after_loop(context):
    print("task after loop")


adhesive.process_start() \
    .task("Loop on empty collection", loop="empty_collection") \
    .task("Task after loop") \
    .process_end() \
    .build(initial_data={
        "empty_collection": []
    })

