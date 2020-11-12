#!/usr/bin/env bash

asciidoctor -o doc/out/index.html\
    -d book \
    -r asciidoctor-diagram \
    doc/usage/index.adoc

cp doc/out/*.svg doc/usage/

asciidoctor-pdf -o doc/out/germanium-usage.pdf \
    -d book \
    -r asciidoctor-diagram \
    doc/usage/index.adoc

rm doc/usage/*.svg
rm doc/out/*.svg.cache

chown raptor:raptor doc/out/*
