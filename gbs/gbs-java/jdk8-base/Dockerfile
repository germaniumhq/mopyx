FROM maven:3.5-jdk-8

RUN useradd -m germanium -u 1000 --user-group --home-dir=/germanium
ENV MAVEN_CONFIG=/germanium/.m2

USER germanium
