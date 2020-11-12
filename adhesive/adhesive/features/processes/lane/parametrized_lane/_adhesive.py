import adhesive


@adhesive.lane(re='docker\: (.*)')
def docker_lane(context, lane_name):
    print(f"created lane {lane_name}")
    yield context.workspace


@adhesive.task('Run java', lane='docker: java')
def run_java(context):
    pass


@adhesive.task('Run maven', lane='docker: maven')
def run_docker_task(context):
    pass


adhesive.build()
