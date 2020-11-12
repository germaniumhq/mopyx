#!/usr/bin/env bash

GERMANIUM_FOLDER=$(readlink -f $(dirname $0)/../..)

RESULT=$(cat $GERMANIUM_FOLDER/Dockerfile  | grep "ENV PYTHON_VERSION" | cut -f2 -d=)

if [[ $1 == "--tag" ]]; then
    echo "python$(echo $RESULT | cut -b1-3)"
else # not [[ $1 == "--tag" ]]
    echo $RESULT
fi   # else [[ $1 == "--tag" ]]

