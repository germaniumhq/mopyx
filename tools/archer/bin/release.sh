#!/usr/bin/env bash

set -e

cd $(readlink -f "$(dirname "$0")/..")

VERSION=$(version-manager --display version)

git tag -f -m "release $VERSION" $VERSION
git push -f github --all
git push -f github --tags

python setup.py sdist upload -r pypitest
python setup.py sdist upload -r pypimain

