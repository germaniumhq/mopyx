import adhesive
from adhesive.workspace import docker, noop


@adhesive.task('Touch a file')
def touch_a_file(context):
	context.workspace.run("""
		touch /tmp/test.txt
	""")

@adhesive.task('Check the file')
def check_the_file(context):
	context.workspace.run("""
		ls -l /tmp/test.txt
	""")


@adhesive.lane('Noop')
def lane_noop(context):
    with noop.inside(context.workspace) as w:
        try:
            print('==> noop')
            yield w
        finally:
            print('<== noop')


@adhesive.lane('Docker')
def lane_docker(context):
    with docker.inside(context.workspace, 'ubuntu:19.04') as w:
        try:
            print("==> docker")
            yield w
        finally:
            print("<== docker")


adhesive.bpmn_build("nested.bpmn")

