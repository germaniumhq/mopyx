from typing import Set

import adhesive
from adhesive import scm, Token

from germanium_docker.pipeline_types import Config


class Data:
    build: Config
    tags_to_push: Set[str]


@adhesive.task('Checkout Code')
def checkout_code(context: Token[Data]) -> None:
    scm.checkout(context.workspace)


@adhesive.task('Build Docker in {loop.key}', loop="build['images']")
def build_docker_image(context: Token[Data]) -> None:
    assert context.loop

    tags = context.loop.value

    if not isinstance(tags, list):
        tags = [tags]

    context.data.tags_to_push = set(tags)

    if not tags:
        raise Exception("Tags for tagging are needed in a docker build")

    context.workspace.run(f"""
        docker build -t {" -t ".join(tags)} {context.loop.key}
    """)


@adhesive.task('Push Docker Image {loop.key}', loop="tags_to_push")
def push_docker_image(context):
    context.workspace.run(f"""
        docker push {context.loop.key}
    """)
