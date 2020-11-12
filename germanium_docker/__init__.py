from typing import cast
import adhesive

from germanium_docker.pipeline_types import Config, ImagesDict, ConfigDict


def pipeline(config: Config) -> None:
    import germanium_docker.steps

    if "images" not in config:
        config = {
            "images": cast(ImagesDict, config)
        }

    config = cast(ConfigDict, config)

    if "push" not in config:
        config["push"] = True

    """
    Builds the docker images
    """
    adhesive.build(initial_data={
        "build": config
    })
