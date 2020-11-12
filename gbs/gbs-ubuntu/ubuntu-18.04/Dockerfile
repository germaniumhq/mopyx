FROM ubuntu:18.04

RUN apt update -y && \
    apt upgrade -y && \
    apt install locales -y && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    LC_LANG="en_US.UTF-8"

RUN useradd -m --home-dir /germanium germanium

USER germanium

