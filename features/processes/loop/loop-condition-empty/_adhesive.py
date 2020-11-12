import adhesive


@adhesive.task('Loop on empty condition')
def loop_on_empty_condition(context):
    raise Exception("shold not execute")


adhesive.process_start() \
    .task("Loop on empty condition", loop="false_value") \
    .process_end() \
    .build(initial_data={
        "false_value": False
    })

