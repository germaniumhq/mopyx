import adhesive
from adhesive.workspace import docker

from workspace import current_dir


@adhesive.task("Basic Task")
def basic_task(context) -> None:
    assert current_dir() == "current dir"


@adhesive.task("Run a ls in the docker workspace")
def run_in_docker_ws(context) -> None:
    with docker.inside(context.workspace, "ubuntu:18.04") as w:
        w.run("ls")


adhesive.build()
