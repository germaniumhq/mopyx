#!/usr/bin/env bash

set -e

git checkout master
git fetch --all
git pull --rebase

PYTHON_VERSIONS="python2.7 python3.4 python3.5"

for PYTHON_VERSION in $PYTHON_VERSIONS; do
    git checkout $PYTHON_VERSION
    git reset --hard origin/$PYTHON_VERSION
done

git checkout master

