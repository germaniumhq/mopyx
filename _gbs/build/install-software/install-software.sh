#!/usr/bin/env bash

set -e

apt update -y
apt upgrade -y

# psmisc has killall
apt install -y curl unzip wget psmisc

#############################################################################
# Install chrome
#############################################################################
cd /tmp
wget --no-proxy https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -y -f install

#############################################################################
# Install firefox
#############################################################################
apt install -y firefox dbus-x11


