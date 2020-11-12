from gbs_pipeline import pipeline_build_gbs_images


pipeline_build_gbs_images({
    "base_containers": {
        "python-2.7": "germaniumhq/python:2.7",
        "python-3.5": "germaniumhq/python:3.5",
        "python-3.6": "germaniumhq/python:3.6",
        "python-3.7": "germaniumhq/python:3.7",
        "python-3.8": ["germaniumhq/python:3.8", "germaniumhq/python:latest"],
        "python-alpine-3.6-build": "germaniumhq/python-alpine:3.6",
        "python-3.6-win32": "germaniumhq/python:3.6-win32",
    },
    "build_containers": {
        "python-build-2.7": "germaniumhq/python-build:2.7",
        "python-build-3.6": "germaniumhq/python-build:3.6",
        "python-build-3.7": "germaniumhq/python-build:3.7",
        "python-build-3.8": ["germaniumhq/python-build:3.8", "germaniumhq/python-build:latest"],
    }
})
