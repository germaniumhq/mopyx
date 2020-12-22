#!/usr/bin/env bash

cd $(readlink -f "$(dirname "$0")/..")
pandoc --from=markdown --to=rst --output=README.rst README.md
