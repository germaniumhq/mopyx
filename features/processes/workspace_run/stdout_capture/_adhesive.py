import adhesive
from adhesive.workspace import docker


@adhesive.task("Stdout capture in local workspace")
def stdout_test_local(context):
    content = context.workspace.run(
        "echo ABC",
        capture_stdout=True)
    assert content == "ABC\n"


adhesive.build()
