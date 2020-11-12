import adhesive


@adhesive.lane('Used Lane')
def used_lane(context):
    yield context.workspace


@adhesive.task('Used Task')
def used_task(context):
    pass


@adhesive.task('Not Used Task')
def not_used_task(context):
    pass


@adhesive.usertask('Not Used UserTask')
def not_used_user(context):
    pass


@adhesive.lane('Not Used Lane')
def not_used_lane(context):
    pass


adhesive.process_start()\
    .task("Used Task", lane="Used Lane")\
    .process_end()\
    .build()
