#!/usr/bin/env bash

fail() {
  echo "FATAL: $1"
  exit -1
}

waitfor() {
  echo "Waiting for file $1 ..."
  while [ ! -f "$1" ]; do
    sleep 1
  done
  echo "found."
}

cd rancher

[ "$CONSUL_TAG" == "" ] && fail "\$CONSUL_TAG is empty"
[ "$TARGET_DOMAIN" == "" ] && fail "\$TARGET_DOMAIN is empty"

HAPROXY_DEFAULT_DEFAULT=http
HAPROXY_TIMEOUT_CONNECT_DEFAULT=2000ms
HAPROXY_TIMEOUT_CLIENT_DEFAULT=15000ms
HAPROXY_TIMEOUT_SERVER_DEFAULT=15000ms

cat haproxy_template.script  | \
  sed -e "s/%HAPROXY_DEFAULT%/${HAPROXY_DEFAULT:-$HAPROXY_DEFAULT_DEFAULT}/g" \
      -e "s/%HAPROXY_TIMEOUT_CONNECT%/${HAPROXY_TIMEOUT_CONNECT:-$HAPROXY_TIMEOUT_CONNECT_DEFAULT}/g" \
      -e "s/%HAPROXY_TIMEOUT_CLIENT%/${HAPROXY_TIMEOUT_CLIENT:-$HAPROXY_TIMEOUT_CLIENT_DEFAULT}/g" \
      -e "s/%HAPROXY_TIMEOUT_SERVER%/${HAPROXY_TIMEOUT_SERVER:-$HAPROXY_TIMEOUT_SERVER_DEFAULT}/g" \
      -e "s/%CONSUL_TAG%/${CONSUL_TAG}/g" \
      -e "s?%TARGET_DOMAIN%?${TARGET_DOMAIN}?g" \
  haproxy_template.script > haproxy_template.consul

# first, run consul-template
rm -f haproxy.pid *.log
touch haproxy.pid

# here, consul must be just the host name, witOUT scheme, but WITH port.
# imPORTant, haha. (stupid fuck)
echo starting consul-template
nohup ./consul-template -wait 5s:10s -consul $CONSUL_ADDRESS:8500 -config ./consul-template.cfg >> consul-template.log 2>&1 &

# we try to do this: http://engineeringblog.yelp.com/2015/04/true-zero-downtime-haproxy-reloads.html
waitfor haproxy.cfg
echo restarting haproxy
./restart_haproxy.sh

# here, consul must be a real url with scheme.
echo starting rancon
nohup rancon rancher consul -c -s url=$CATTLE_CONFIG_URL -b url=http://$CONSUL_ADDRESS >> rancon.log 2>&1 &

echo starting tail
waitfor haproxy.log
waitfor rancon.log
waitfor consul-template.log
exec tail -n 100 -f *.log
