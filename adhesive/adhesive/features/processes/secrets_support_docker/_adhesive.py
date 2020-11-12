import adhesive
from adhesive.secrets import secret
from adhesive.workspace import docker


@adhesive.task("Test Secret On Docker Workspace")
def test_secret_on_docker_workspace(context):
    with docker.inside(context.workspace, "ubuntu:18.04") as w:
        with secret(w, "SECRET_FILE", "/tmp/super-docker/secret.file"):
            w.run("cat /tmp/super-docker/secret.file")


adhesive.build()
