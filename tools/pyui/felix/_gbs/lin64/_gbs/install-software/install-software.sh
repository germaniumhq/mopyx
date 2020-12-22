set -e

apt update -y
apt upgrade -y
apt install -y wget

#############################################################################
# Install chrome
#############################################################################
cd /tmp
wget --no-proxy https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -y -f install


