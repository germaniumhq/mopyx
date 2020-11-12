from typing import Optional

import adhesive
from adhesive.workspace import docker
import textwrap
import logging

LOG = logging.getLogger(__name__)


tools = {
    "mypy": textwrap.dedent("""\
        FROM germaniumhq/python:3.8
        ENV REFRESHED_AT 2018.10.14-06:56:31
        RUN pip install mypy mypy_extensions grpc_stubs adhesive
        """),

    "ansible": textwrap.dedent("""\
        FROM germaniumhq/python:3.8
        ENV REFRESHED_AT 2018.10.14-06:58:16
        RUN pip install ansible
    """),

    "flake8": textwrap.dedent("""\
        FROM germaniumhq/python:3.8
        ENV REFRESHED_AT 2020-04-20-17:21:47
        RUN pip install flake8
    """),

    "black": textwrap.dedent("""\
        FROM germaniumhq/python:3.8
        ENV REFRESHED_AT 2020-04-20-17:21:27
        RUN pip install black==20.8b1
    """),

    "python": textwrap.dedent("""\
        FROM germaniumhq/python:3.8
    """),

    "behave": textwrap.dedent("""\
        FROM python:3.8

        RUN pip install behave
        RUN curl https://get.docker.com | sh
    """),

    "git": textwrap.dedent("""\
        FROM germaniumhq/ubuntu:18.04
        ENV REFRESHED_AT 2018.10.18-05:25:08
        USER root
        RUN apt update -y && apt install -y git && rm -rf /var/lib/apt/lists/*
        USER germanium
    """),

    "version-manager": textwrap.dedent("""\
        FROM germaniumhq/python:3.8
        RUN pip install vm==2.5.1
    """)
}


def ensure_tooling(context, tool_name) -> None:
    w = context.workspace

    if tool_name == "flake8":
        LOG.warning("flake8 is deprecated as a tool. Use black.")

    with w.temp_folder():
        w.write_file("Dockerfile", tools[tool_name])
        w.run(f"docker build -t germaniumhq/tools-{tool_name}:latest .")


def run_tool(context,
             *,
             tool: str,
             command: str,
             capture_stdout: Optional[bool] = None) -> str:
    with docker.inside(
            context.workspace,
            f"germaniumhq/tools-{tool}",
            extra_docker_params="-v /var/run/docker.sock:/var/run/docker.sock") as w:
        return w.run(command, capture_stdout=capture_stdout)


def image_name(tool: str) -> str:
    """
    Returns the docker image name for a tool
    """
    return f"germaniumhq/tools-{tool}"
