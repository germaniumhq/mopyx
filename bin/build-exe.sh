#!/usr/bin/env bash

DOCKER_IMAGE="ciplogic/pyinstaller-windows:python3"

docker run -it \
    --rm \
    -v $(readlink -f $(dirname $(readlink -f "$0"))/..):/src \
    $DOCKER_IMAGE

