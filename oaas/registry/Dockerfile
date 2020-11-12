FROM python:3.8

COPY / /src

RUN cd /src && \
    pip install -r requirements.txt && \
    python -m unittest
