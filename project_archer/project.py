import sys
import io
from contextlib import redirect_stdout, redirect_stderr

import project_archer.environment.read_shell_parameters as read_shell_parameters
from project_archer.environment.environment import BashEnvironment
from project_archer.operations.clear_zone import clear_zone

from project_archer.operations.list_projects import list_projects
from project_archer.operations.create_project import create_new_project
from project_archer.operations.edit_project import edit_project
from project_archer.operations.empty_run import empty_project_run
from project_archer.operations.select_project import select_project
from project_archer.operations.select_zone import select_zone

env = BashEnvironment()

args = None
out = io.StringIO()
err = io.StringIO()
try:
    with redirect_stdout(out), redirect_stderr(err):
        args = read_shell_parameters.parser.parse_args()
except SystemExit:
    if out.getvalue():
        env.log(out.getvalue().strip())
    if err.getvalue():
        env.log(err.getvalue().strip())

if args:
    if args.list:
        list_projects(args, env)
    elif args.new:
        create_new_project(args, env)
    elif args.edit:
        edit_project(args, env)
    elif args.zone:
        select_zone(args, env)
    elif args.zone_clear:
        clear_zone(args, env)
    else:  # project selection or empty run
        if not args.project:
            empty_project_run(args, env)
        else:
            select_project(args, env)

env.flush()
