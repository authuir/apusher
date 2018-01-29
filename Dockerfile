FROM alpine:latest

MAINTAINER i@authuir.com

ENV APUSHER_HOME="/opt/apusher"\
    APUSHER_VERSION=1.0

WORKDIR ${APUSHER_HOME}

RUN apk update && apk add py-pip
RUN apk add python3
RUN apk add git
RUN apk add libsodium
RUN pip3 install pysocks
RUN pip3 install requests

RUN cd /opt && git clone https://github.com/authuir/apusher.git

COPY ./config.json /opt/apusher/config.json

WORKDIR ${APUSHER_HOME}

ENTRYPOINT python3 /opt/apusher/monitor.py