from termcolor_util import red

from project_archer.environment.environment import BashEnvironment
from project_archer.operations.list_projects import list_projects


def select_zone(args, env: BashEnvironment):
    select_zone_str(args=args, env=env, zone=args.zone)


def select_zone_str(*, args, env: BashEnvironment, zone: str):
    env.log(red("zone ", bold=True), newline=False)
    env.set_envvar(
        "CIPLOGIC_ARCHER_CURRENT_" + args.internalRunMode.upper() + "_ZONE", zone
    )

    list_projects(args, env, custom_zone=zone)
