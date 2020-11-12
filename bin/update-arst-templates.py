#!/usr/bin/env python3

import pathlib
import subprocess

FOLDERS = [
    "python-2.7-build",
    "python-2.7-test",
    "python-3.4-build",
    "python-3.4-test",
    "python-3.5-build",
    "python-3.5-test",
    "python-3.6-build",
    "python-3.6-test",
]
CURRENT_FOLDER = pathlib.Path(__file__).resolve().parent.parent


def update_arst(folder_name: str) -> None:
    subprocess.check_call(
        [
            "arst",
            "--auto"
        ],
        cwd=f"{CURRENT_FOLDER}/{folder_name}")


def main() -> None:
    for folder in FOLDERS:
        update_arst(folder)


if __name__ == '__main__':
    main()
