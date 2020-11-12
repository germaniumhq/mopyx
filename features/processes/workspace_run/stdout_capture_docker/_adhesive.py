import adhesive
from adhesive.workspace import docker


@adhesive.task("Stdout capture in docker workspace")
def stdout_test_in_docker(context):
    with docker.inside(context.workspace, "ubuntu:18.04") as w:
        content = w.run(
            "echo ABC",
            capture_stdout=True)

    assert content == "ABC\n"


adhesive.build()
