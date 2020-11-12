from project_archer.environment.read_shell_parameters import current_project
from project_archer.operations.list_projects import list_projects


def empty_project_run(args, env):
    project = current_project(args.internalRunMode)
    if project:
        project_name = project
    else:
        project_name = "<none>"

    list_projects(args, env)
    env.log("Current " + args.internalRunMode + ": " + project_name)
