#!/usr/bin/env bash

PYTHON_VERSIONS="python2.7 python3.4 python3.5"

set -e

git checkout master

GERMANIUM_FOLDER=$(readlink -f $(dirname $0)/..)

for PYTHON_VERSION in $PYTHON_VERSIONS; do
    git checkout $PYTHON_VERSION
    git rebase master
    docker build -t germanium/germanium-$PYTHON_VERSION .
    docker run --rm -it -v $GERMANIUM_FOLDER/features:/tests/features:ro -e TEST_REUSE_BROWSER=1 germanium/germanium-$PYTHON_VERSION
done

git checkout master

