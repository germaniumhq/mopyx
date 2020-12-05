import os

from project_archer.environment.read_shell_parameters import project_folder


def create_new_project(args, env):
    folder = project_folder(args)

    env.execute("mkdir -p " + folder)
    env.execute("$EDITOR " + os.path.join(folder, args.new + ".yml"))
