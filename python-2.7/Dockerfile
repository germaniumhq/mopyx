FROM ubuntu:16.04

RUN apt update -y && \
    apt upgrade -y && \
    apt install python python-pip python-dev binutils zlib1g locales -y && \
    pip install virtualenv && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    LC_LANG="en_US.UTF-8"

RUN useradd -m --home-dir /germanium germanium && \
    python -m virtualenv /python && \
    chown -R germanium:germanium /python

USER germanium
ENV PATH="/python/bin:${PATH}"
