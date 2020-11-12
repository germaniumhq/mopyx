#!/usr/bin/env python3
import sys

import click

from git_monorepo.move_command import move
from git_monorepo.pull_command import pull
from git_monorepo.push_command import push


@click.group()
def main():
    pass


# define the pull command
pull = click.argument("folders", nargs=-1)(pull)
pull = click.option(
    "--sync/--no-sync", default=True, help="Update the .monorepo.sync file"
)(pull)
pull = click.option(
    "--required/--no-required",
    default=False,
    help="Pull only repos that have changes from upstream",
)(pull)
click_pull = click.command("pull")(pull)

# define the push command
push = click.option(
    "--resync/--no-resync",
    default=False,
    help="Push all repos even if .monorepo.sync says they're not changed",
)(push)
click_push = click.command("push")(push)

# define the move command
move = click.argument("new_path")(move)
move = click.argument("old_path")(move)
click_move = click.command("mv")(move)


@click.command("help")
@click.argument("command")
def help(command) -> None:
    with click.Context(main) as ctx:  # type: ignore
        if "pull" == command:
            click.echo(click_pull.get_help(ctx))
        elif "push" == command:
            click.echo(click_push.get_help(ctx))
        else:
            click.echo(f"Unknown command {command}")
            sys.exit(1)


main.add_command(click_pull)
main.add_command(click_push)
main.add_command(click_move)
main.add_command(help)


if __name__ == "__main__":
    main()
