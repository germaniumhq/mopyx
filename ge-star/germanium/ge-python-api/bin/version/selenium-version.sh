#!/usr/bin/env bash

GERMANIUM_FOLDER=$(readlink -f $(dirname $0)/../..)

cat $GERMANIUM_FOLDER/setup.py  | grep install_requires | grep selenium | cut -f4 -d= | cut -f1 -d\'

