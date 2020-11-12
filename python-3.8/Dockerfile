# compiled by docker-optimizer
# https://github.com/bmustiata/docker-optimizer
from ubuntu:18.04
env LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8" LC_LANG="en_US.UTF-8" PATH="/python/bin:$PATH"
run apt update -y && apt upgrade -y && apt install -y locales &&     locale-gen en_US.UTF-8 && apt install -y software-properties-common &&     add-apt-repository ppa:deadsnakes/ppa -y &&     apt update -y && apt install -y         python         python3.8-venv         python3.8-dev         binutils         git         build-essential         zlib1g-dev && python3.8 -m ensurepip &&     pip3.8 install virtualenv &&     rm -rf /var/lib/apt/lists/* && useradd -m --home-dir /germanium germanium &&     python3.8 -m virtualenv /python &&     chown -R germanium:germanium /python && chgrp -R 0 /python &&     chmod -R g=u /python &&     chgrp -R 0 /germanium &&     chmod -R g=u /germanium
user 1000
