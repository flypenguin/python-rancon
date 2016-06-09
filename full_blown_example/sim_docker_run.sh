#!/usr/bin/env bash

# change this
CONSUL_VERSION="0.14.0"

# ... and this ONLY IF NEEDED.
CONSUL_URL="https://releases.hashicorp.com/consul-template/${CONSUL_VERSION}/consul-template_${CONSUL_VERSION}_linux_amd64.zip"


cd "$(dirname $0)/.."
pwd

rm -rf rancher_run
cp -r rancher rancher_run

cd rancher_run

curl -sl $CONSUL_URL -o consul.zip
unzip consul.zip
rm consul.zip

exec ./startup.sh
