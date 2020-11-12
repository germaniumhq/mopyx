FROM ubuntu:16.04

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    apt install -y python3 python3-pip python3-dev binutils && \
    pip3 install virtualenv && \
    rm -rf /var/lib/apt/lists/*

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    LC_LANG="en_US.UTF-8"

RUN useradd -m --home-dir /germanium germanium && \
    python3 -m virtualenv /python && \
    chown -R germanium:germanium /python

ENV PATH="/python/bin:$PATH"

USER germanium

