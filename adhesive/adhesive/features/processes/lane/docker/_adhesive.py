import adhesive
from adhesive.workspace import docker


@adhesive.lane("Docker Container")
def lane_docker_container(context):
    with docker.inside(context.workspace, "ubuntu:19.04") as w:
        yield w


@adhesive.task(re="^Touch File: (.*)$")
def touch_file(context, file_name):
    context.workspace.run(f"""
        touch {file_name}
    """)


@adhesive.task(re="^Check if File Exists: (.*)$")
def check_file_exists(context, file_name):
    print(context.workspace)
    context.workspace.run(f"""
        ls -l {file_name}
    """)


adhesive.bpmn_build("lane.bpmn")
