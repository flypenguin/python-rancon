#!/usr/bin/env bash

cd "$(dirname $0)"
docker run -d -p 8080:8080 -p 80:80 --name traefik -v $PWD/traefik.toml:/etc/traefik/traefik.toml traefik

