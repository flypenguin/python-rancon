#!/usr/bin/env bash

# use this script for the rancher catalog service

exec /usr/src/app/rancon.py rancher consul -cw5 -s url=${CATTLE_URL} $@
