from termcolor_util import red

from project_archer.environment.environment import BashEnvironment
from project_archer.operations.list_projects import list_projects


def clear_zone(args, env: BashEnvironment):
    env.log(red("zone cleared", bold=True))
    env.unset_envvar(
        "CIPLOGIC_ARCHER_CURRENT_" + args.internalRunMode.upper() + "_ZONE"
    )

    list_projects(args, env, custom_zone="")  # this also flushes

    # env.flush()
