FROM python:3.8-alpine

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    LC_LANG="en_US.UTF-8"

RUN apk add git curl docker-cli && \
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl && \
    mv kubectl /usr/local/bin && \
    chmod +x /usr/local/bin/kubectl && \
    pip3 install adhesive==1.5.0 mypy_extensions

