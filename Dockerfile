FROM python:3-onbuild

MAINTAINER Axel Bock <mr.axel.bock@gmail.com>

EXPOSE 80 443 8080 5000

ENV consul_version 0.14.0
ENV consul_url https://releases.hashicorp.com/consul-template/${consul_version}/consul-template_${consul_version}_linux_amd64.zip

RUN  \
       apt-get update && apt-get install -y haproxy unzip \
    && rm -rf rancher_run ; cp -r rancher rancher_run \
    && cd rancher_run \
    && curl -ls $consul_url -o consul.zip \
    && unzip consul.zip \
    && rm *.zip

WORKDIR rancher_run
ENTRYPOINT startup.sh
