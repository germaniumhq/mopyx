from adhesive.workspace.Workspace import Workspace


def checkout(workspace: Workspace) -> None:
    workspace.copy_to_agent(
        ".",
        workspace.pwd,
    )
