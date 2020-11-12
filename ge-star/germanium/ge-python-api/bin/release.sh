#!/usr/bin/env bash

#
# Just a tiny script to do all the rebases, and check
# all supported versions of python.
#

set -e
set -x

VERSION=2.0.11

PYTHON_VERSIONS="python2.7 python3.4 python3.5 python3.6"

git tag -f "$VERSION" master -m "release $VERSION"
for PYTHON_VERSION in $PYTHON_VERSIONS; do
    git tag -f "$VERSION-$PYTHON_VERSION" $PYTHON_VERSION -m "release $VERSION-$PYTHON_VERSION"
done

git push origin --all
git push github --all

echo '#############################################################################'
echo '# Pushing Germanium Python 3 to PyPI'
echo '#############################################################################'
py 3
git checkout master
python setup.py bdist_wheel upload -r pypitest
python setup.py bdist_wheel upload -r pypimain

echo '#############################################################################'
echo '# Pushing Germanium Python 2 to PyPI'
echo '#############################################################################'
py 2
git checkout python2.7
python setup.py bdist_wheel upload -r pypitest
python setup.py bdist_wheel upload -r pypimain

