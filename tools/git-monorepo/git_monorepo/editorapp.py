#!/usr/bin/env python

import os

import click


@click.command()
@click.argument("edited_file")
def main(edited_file: str) -> None:
    """
    This code does nothing on purpose. This is to be used as a git
    editor, and automatically commit the files.
    """
    custom_message = os.environ.get("GIT_MONOREPO_EDITOR_MESSAGE", "")

    if not custom_message:
        return

    # we write the custom message at the top
    message = [custom_message]

    with open(edited_file, "rt", encoding="utf-8") as f:
        for line in f.readlines():
            if not line.startswith("#"):
                message.append(line)

    with open(edited_file, "wt", encoding="utf-8") as f:
        f.write("\n".join(message))


if __name__ == "__main__":
    main()
