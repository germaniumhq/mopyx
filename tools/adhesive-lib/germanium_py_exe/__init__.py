import adhesive
import os
import addict  # type: ignore

from germanium_py_exe.pipeline_types import PipelineConfig
from germanium_py_exe.steps import *  # type: ignore


def pipeline(build: PipelineConfig) -> None:
    script_dir = os.path.dirname(__file__)

    build_data = addict.Dict(build)

    if not "run_mypy" in build_data:
        build_data.run_mypy = True

    if not "run_flake8" in build_data:
        build_data.run_flake8 = True

    if not "run_black" in build_data:
        build_data.run_black = True

    if build_data.repo and not isinstance(build_data.repo, list):
        build_data.repo = [ build_data.repo ]

    if not isinstance(build_data.binaries, list):
        build_data.binaries = [ build_data.binaries ]

    adhesive.bpmn_build(
        os.path.join(script_dir, "build_python.bpmn"),
        initial_data={
            "build": build_data
        })

