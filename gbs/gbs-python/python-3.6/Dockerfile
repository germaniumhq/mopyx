FROM ubuntu:16.04

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt update -y && \
    apt install -y \
        python \
        python3.6-venv \
        python3.6-dev \
        binutils \
        git \
        build-essential \
        zlib1g-dev \
        locales && \
    python3.6 -m ensurepip && \
    pip3.6 install virtualenv && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    LC_LANG="en_US.UTF-8"

RUN useradd -m --home-dir /germanium germanium && \
    python3.6 -m virtualenv /python && \
    chown -R germanium:germanium /python

ENV PATH="/python/bin:$PATH"

USER germanium

