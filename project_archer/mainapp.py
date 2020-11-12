#!/usr/bin/python3
import sys

from project_archer.environment.environment import BashEnvironment


def main():
    run_mode = None

    env = BashEnvironment()

    if len(sys.argv) <= 1:
        print(
            """You need to define a run mode, e.g.:

        $ . archer.py
        $ project -n test
        $ project test"""
        )
        quit(1)

    for run_mode in sys.argv[1:]:
        env.define_command(
            run_mode,
            'eval "$(%s -m project_archer.project --internalRunMode=%s $@)"'
            % ("python3", run_mode),
        )

    env.flush()


if __name__ == "__main__":
    main()
