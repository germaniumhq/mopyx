#!/usr/bin/env bash

# This script can't be sourced since it depends on its
# location to find other scripts.

set -e

PIPY_URL=$1
PIPY_INDEX_URL=$2

GERMANIUM_FOLDER=$(readlink -f $(dirname $0)/..)
TAG_VERSION=$($GERMANIUM_FOLDER/bin/version/python-version.sh --tag)

cd $GERMANIUM_FOLDER

echo "Sending arguments to the docker build:"
echo "pypi_url is $PIPY_URL"
echo "pypi_index_url is $PIPY_INDEX_URL"


cat << EOM
Going to RUN:
docker build \
    -t germanium/germanium-$TAG_VERSION \
    --build-arg pypi_url=$PIPY_URL \
    --build-arg pypi_index_url=$PIPY_INDEX_URL \
    --network host \
    .
EOM

docker build \
    -t germanium/germanium-$TAG_VERSION \
    --build-arg pypi_url=$PIPY_URL \
    --build-arg pypi_index_url=$PIPY_INDEX_URL \
    --network host \
    .

cd $GERMANIUM_FOLDER/features

docker build -t germanium/germanium-${TAG_VERSION}-tests .

