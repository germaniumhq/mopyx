#!/usr/bin/env bash

cd /tmp/wine-tmp

echo "Cleaning up: $f"
find / -name api-ms-win-core-path-l1-1-0.dll\* | xargs rm -f

#############################################################################
# Remove all files packaged in the Visual Studio runtime files.
#############################################################################

for f in `ls *.dll`; do
    TO_REMOVE=$(find /opt/wine-stable -name "$f*")
    echo "Cleaning up: $f -> removing $TO_REMOVE"
    rm -f $TO_REMOVE
done

