FROM centos:7

MAINTAINER i@authuir.com

ENV APUSHER_HOME="/opt/apusher"\
    APUSHER_VERSION=1.0

WORKDIR ${APUSHER_HOME}

RUN yum -y update
RUN yum install -y yum-utils
RUN yum install -y epel-release
RUN yum install -y python34 
RUN yum install -y libsodium-devel
RUN yum install -y git
RUN yum install -y python34-setuptools
RUN easy_install-3.4 pip
RUN pip3 install pysocks
RUN pip3 install requests

RUN cd /opt && git clone https://github.com/authuir/apusher.git

COPY ./config.json /opt/apusher/config.json

WORKDIR ${APUSHER_HOME}

ENTRYPOINT python3 /opt/apusher/monitor.py