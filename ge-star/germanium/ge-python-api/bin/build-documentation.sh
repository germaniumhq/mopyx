#!/usr/bin/env bash

GERMANIUM_FOLDER=$(readlink -f $(dirname $0)/..)

echo $GERMANIUM_FOLDER

docker run --rm \
    -v $GERMANIUM_FOLDER:/documents \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    asciidoctor/docker-asciidoctor \
    bin/build-documentation-inside-docker.sh

