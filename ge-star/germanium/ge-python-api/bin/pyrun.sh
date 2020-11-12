#!/usr/bin/env bash

GERMANIUM_PATH="/home/raptor/projects/germanium/germanium"
CURRENT_PYTHON_PATH=`echo "import sys; print(':'.join(sys.path))" | python -`

NEW_PYTHON_PATH="${GERMANIUM_PATH}$CURRENT_PYTHON_PATH"

echo "Running with path: $NEW_PYTHON_PATH"

export PYTHONPATH="$NEW_PYTHON_PATH"
python $@

