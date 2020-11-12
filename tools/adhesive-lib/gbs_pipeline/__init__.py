from typing import List, Any

import adhesive
from adhesive import scm
from adhesive.workspace import docker

import ge_tooling  # this defines the Ensure Tooling, and Run tool steps.


def ensure_list(item: Any) -> List:
    if isinstance(item, list):
        return item

    return [item]


@adhesive.task("Checkout Code")
def checkout_code(context) -> None:
    scm.checkout(context.workspace)


@adhesive.task('Collect Images to Push')
def collect_images_to_push(context):
    context.data.containers_to_push = []

    for key, value in context.data.base_containers.items():
        context.data.containers_to_push.extend(ensure_list(value))

    for key, value in context.data.build_containers.items():
        context.data.containers_to_push.extend(ensure_list(value))


@adhesive.task(re=r"^Ensure Tooling:\s+(.+)$")
def ensure_tooling(context, tool_name) -> None:
    ge_tooling.ensure_tooling(context, tool_name)


@adhesive.task("Run Tool: behave")
def run_tool(context) -> str:
    ge_tooling.run_tool(
            context,
            tool="behave",
            command="behave")


@adhesive.task("Fetch Base Images")
def fetch_base_images(context) -> None:
    pass


@adhesive.task(re=[
        "Create Base Image Image .*?",
        "Create Build Image Image .*?",
])
def build_docker_image(context) -> None:
    with context.workspace.chdir(context.loop.key):
        docker.build(context.workspace,
                     context.loop.value)


@adhesive.task("Test Images")
def test_containers(context) -> None:
    with docker.inside(context.workspace,
                       f"germaniumhq/tools-{tool_name}") as w:
        w.run("behave")


@adhesive.task("Push Image {loop.value}")
def push_containers(context) -> None:
    context.workspace.run(f"""
        docker push {context.loop.value}
    """)


def pipeline_build_gbs_images(config):
    if 'build_containers' not in config:
        config['build_containers'] = dict()

    if 'base_containers' not in config:
        config['base_containers'] = dict()

    adhesive.process_start()\
        .branch_start()\
            .task("Checkout Code")\
            .task("Fetch Base Images")\
        .branch_end()\
        .branch_start()\
            .task("Ensure Tooling: behave")\
        .branch_end()\
        .branch_start()\
            .task("Collect Images to Push")\
        .branch_end()\
        .subprocess_start("Base Images")\
            .task("Create Base Image Image {loop.key}", loop="base_containers")\
        .subprocess_end()\
        .subprocess_start("Base Images")\
            .task("Create Build Image Image {loop.key}", loop="build_containers")\
        .subprocess_end()\
        .task("Run Tool: behave")\
        .task("Push Image {loop.value}", loop="containers_to_push")\
    .process_end()\
    .build(initial_data=config)

