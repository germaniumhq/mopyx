#!/usr/bin/env python3

import re
import subprocess
import os.path
from typing import List

import click
from termcolor_util import yellow

FOLDER = "grpc"
EXTENSION = ".proto"

IMPORT_RE = re.compile(r"^(import )(.+? as .*)$", re.MULTILINE)
ASSIGNMENT_RE = re.compile(r"^(def add_)(.+?)(_)(to_server\(servicer, server\):)$")


@click.command()
@click.argument("grpc_files", nargs=-1)
@click.option("--module", help="The module of the python package to generate")
@click.option("--output", help="Output folder where to write the files", default=".")
def main(grpc_files: List[str], module: str, output: str) -> None:
    for grpc_file in grpc_files:
        grpc_compile(output, module, grpc_file)


def grpc_compile(
    output_folder: str,
    module_name: str,
    grpc_file: str,
) -> None:
    """
    Compiles the files from the generated proto files
    """
    base_grpc_file = os.path.splitext(os.path.basename(grpc_file))[0]
    generated_grpc_file = os.path.join(output_folder, base_grpc_file + "_pb2_grpc.py")
    generated_proto_file = os.path.join(output_folder, base_grpc_file + "_pb2.py")
    generated_proto_pyi = os.path.join(output_folder, base_grpc_file + "_pb2.pyi")

    print(
        yellow("COMPILING"),
        yellow(grpc_file, bold=True),
        yellow("->"),
        yellow(generated_grpc_file, bold=True),
        yellow(","),
        yellow(generated_proto_file, bold=True),
        yellow(","),
        yellow(generated_proto_pyi, bold=True),
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
            os.curdir,
            "-I",
            os.path.dirname(grpc_file),
            f"--python_out={output_folder}",
            f"--grpc_python_out={output_folder}",
            f"--mypy_out={output_folder}",
            grpc_file,
        ]
    )

    # ####################################################################
    # Prepare the content to OaaS with a static method on the type, and
    # patch the imports because the generator can't do it
    # ####################################################################
    with open(generated_grpc_file, "rt", encoding="utf-8") as f:
        content = f.read()

        # In OaaS we register as clients directly the type. Unfortunately,
        # to add them into a grpc server we need to use the generated
        # add_to_server
        new_content = convert_to_static_method(content)

        # We override the module name only if there is a custom module
        # passed
        if module_name:
            new_content = IMPORT_RE.sub(f"\\1 {module_name}.\\2", new_content)

    with open(generated_grpc_file, "wt", encoding="utf-8") as f:
        f.write(new_content)

    # ####################################################################
    # Run black over the final sources
    # ####################################################################
    subprocess.check_call(
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


if __name__ == "__main__":
    main()
