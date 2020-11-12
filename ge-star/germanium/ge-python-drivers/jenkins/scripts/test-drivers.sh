#!/usr/bin/env bash

# fail fast
set -e

#############################################################################
# Run the actual tests on the binary drivers
#############################################################################
TAGS="placeholder"

if [[ "$RUN_CHROME_TESTS" == "true" ]]; then
    TAGS="$TAGS,chrome"
fi # [[ "$RUN_CHROME_TESTS" == "true" ]]

if [[ "$RUN_FIREFOX_TESTS" == "true" ]]; then
    TAGS="$TAGS,firefox"
fi # [[ "$RUN_FIREFOX_TESTS" == "true" ]]

behave -t $TAGS

