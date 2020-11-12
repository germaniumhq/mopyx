import adhesive
from adhesive.secrets import secret
from adhesive.execution.ExecutionToken import ExecutionToken


@adhesive.task("Test Secret On Local Workspace")
def test_secret_on_local_workspace(context: ExecutionToken):
    with secret(context.workspace,
                "SECRET_FILE",
                "/tmp/super-secret/secret.file"):
        context.workspace.run("cat /tmp/super-secret/secret.file")


adhesive.build()
