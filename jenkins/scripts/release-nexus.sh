#!/usr/bin/env bash

# fail fast
set -e

# we source to set the right environment
. /home/ciplogic/python/bin/activate

#############################################################################
# Utility functions.
#############################################################################
function deactivate_proxy() {
    old_http_proxy="$http_proxy"
    old_https_proxy="$https_proxy"
    old_ftp_proxy="$ftp_proxy"
    unset http_proxy
    unset https_proxy
    unset ftp_proxy
}

function activate_proxy() {
    export http_proxy="$old_http_proxy"
    export https_proxy="$old_https_proxy"
    export ftp_proxy="$old_ftp_proxy"
}

deactivate_proxy

#############################################################################
# Do the actual publish
#############################################################################

# make sure we know about the nexus package index
cp /scripts/_pypirc_nexus /home/ciplogic/.pypirc

# publish
cd /tmp/project
python setup.py sdist upload -r nexus
