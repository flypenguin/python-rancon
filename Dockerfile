FROM python:3-onbuild

MAINTAINER Axel Bock <mr.axel.bock@gmail.com>

EXPOSE 80 443 8080 5000

RUN  \
       cd rancher
    && wget -nd https://releases.hashicorp.com/consul-template/0.14.0/consul-template_0.14.0_linux_amd64.zip \
    && unzip consul_template_0.14.0_linux_amd64.zip \
    && rm *.zip \
    && apt-get update && apt-get install -y haproxy

ENTRYPOINT ./rancher/startup.sh
