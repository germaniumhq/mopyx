#!/usr/bin/env python3

import os
import subprocess
import logging
import re

from termcolor_util import cyan, yellow

FOLDER = "grpc"
EXTENSION = ".proto"

IMPORT_RE = re.compile(r"^(import )(.+? as .*)$", re.MULTILINE)
ASSIGNMENT_RE = re.compile(r"^(def add_)(.+?)(_)(to_server\(servicer, server\):)$")


def main() -> None:
    files_changed = False

    for f in os.listdir(FOLDER):
        if not f.endswith(EXTENSION):
            continue

        grpc_file = os.path.join(FOLDER, f)
        generated_proto_file = find_target_file(grpc_file, suffix="_pb2.py")
        generated_proto_pyi = find_target_file(grpc_file, suffix="_pb2.pyi")
        generated_grpc_file = find_target_file(grpc_file, suffix="_pb2_grpc.py")

        if is_newer(grpc_file, generated_proto_file) and is_newer(
            grpc_file, generated_grpc_file
        ):
            print(
                cyan("IGNORED", bold=True),
                cyan(grpc_file, bold=True),
                cyan("is older than both"),
                cyan(generated_proto_file, bold=True),
                cyan("and"),
                cyan(generated_grpc_file, bold=True),
            )
            continue

        files_changed = True
        grpc_compile(
            grpc_file, generated_grpc_file, generated_proto_file, generated_proto_pyi
        )


def find_target_file(grpc_file: str, suffix: str) -> str:
    # 3:-3 - remove FOLDER from prefix, and EXTENSION from suffix of the file
    python_file = grpc_file[len(FOLDER) + 1 : -(len(EXTENSION))] + suffix
    return os.path.join("oaas_simple", "rpc", python_file)


def is_newer(base: str, expected_newer: str) -> True:
    """
    Checks if the expected_newer file is newer than base.
    """
    if not os.path.isfile(base):
        raise Exception(f"{base} is not a file")

    if not os.path.isfile(expected_newer):
        return False

    base_last_modified = get_last_modified(base)
    expected_last_modified = get_last_modified(expected_newer)

    if base_last_modified < expected_last_modified:
        return True

    return False


def grpc_compile(
    grpc_file: str,
    generated_grpc_file: str,
    generated_proto_file: str,
    generated_proto_pyi: str,
) -> None:
    """
    Compiles the UI using pyside2-uic, the python code generator from
    the UI files.
    """
    print(
        yellow("COMPILING"),
        yellow(grpc_file, bold=True),
        yellow("->"),
        yellow(generated_grpc_file, bold=True),
        yellow(","),
        yellow(generated_proto_file, bold=True),
    )

    # ####################################################################
    # Generate the actual sources
    # ####################################################################
    subprocess.check_call(
        [
            "python",
            "-m",
            "grpc_tools.protoc",
            "-I",
            FOLDER,
            "--python_out=oaas_simple/rpc/",
            "--grpc_python_out=oaas_simple/rpc",
            "--mypy_out=oaas_simple/rpc",
            grpc_file,
        ]
    )

    # ####################################################################
    # Patch the imports because the generator can't do it, and prepare
    # for OaaS.
    # ####################################################################
    with open(generated_grpc_file, "rt", encoding="utf-8") as f:
        content = f.read()

        new_content = IMPORT_RE.sub(r"\1 oaas_simple.rpc.\2", content)

        # In OaaS we register as clients directly the type. Unfortunately,
        # to add them into a grpc server we need to use the generated
        # add_to_server
        new_content = convert_to_static_method(new_content)

    with open(generated_grpc_file, "wt", encoding="utf-8") as f:
        f.write(new_content)

    # ####################################################################
    # Run black over the final sources
    # ####################################################################
    subprocess.call(
        [
            "python",
            "-m",
            "black",
            generated_grpc_file,
            generated_proto_file,
            generated_proto_pyi,
        ]
    )


def convert_to_static_method(new_content: str) -> str:
    lines = new_content.split("\n")
    index = 0

    while index < len(lines):
        m = ASSIGNMENT_RE.match(lines[index])

        if not m:
            index += 1
            continue

        lines[index] = m.group(1) + m.group(4)
        lines.insert(index, "@staticmethod")

        while lines[index]:
            lines[index] = "    " + lines[index]
            index += 1

        index += 1

    return "\n".join(lines)


def get_last_modified(file_name: str) -> int:
    return os.path.getmtime(file_name)


if __name__ == "__main__":
    main()
