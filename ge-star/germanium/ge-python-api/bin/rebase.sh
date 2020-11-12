#!/usr/bin/env bash

#
# Just a tiny script to do all the rebases, and check
# all supported versions of python.
#

set -e

VERSION=$1

PYTHON_VERSIONS="python2.7 python3.4 python3.5"

for PYTHON_VERSION in $PYTHON_VERSIONS; do
    git checkout $PYTHON_VERSION
    git rebase master
done

git checkout master

