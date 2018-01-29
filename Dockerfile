FROM centos:7

RUN yum -y update
RUN yum install -y yum-utils
RUN yum install -y epel-release
RUN yum install -y python34
RUN yum install -y libsodium-devel
RUN yum install -y wget

