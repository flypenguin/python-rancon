#!/usr/bin/env bash

# WE NEED THE FOLLOWING ENV VARIABLES:
#
#     CONSUL_TAG - services with this tag in consul are picked up by
#                  haproxy and load balanced
#
#     CONSUL_ADDRESS - the address of the consul service. must be a single
#                      host name, without scheme or port information
#                      (example: 'consul-server')
#                      NOTE: consul *MUST* run on port 8500!!
#
#     TARGET_DOMAIN - the domain to compare to (SERVICE.TARGET_DOMAIN)
#
#     CATTLE_CONFIG_URL - the URL to the rancher API
#                         (example: 'http://rancher.my.domain/v1')

set -e

fail() {
  echo -e "FATAL: $1"
  exit -1
}

waitfor() {
  echo "Waiting for file $1 ..."
  while [ ! -f "$1" ]; do
    sleep 1
  done
  echo "found."
}

ERROR=""
[ "$CONSUL_TAG" == "" ] && ERROR="${ERROR}\n - \$CONSUL_TAG is empty"
[ "$TARGET_DOMAIN" == "" ] && ERROR="${ERROR}\n - \$TARGET_DOMAIN is empty"
[ "$CONSUL_ADDRESS" == "" ] && ERROR="${ERROR}\n - \$CONSUL_ADDRESS is empty"
[ "$CATTLE_CONFIG_URL" == "" ] && ERROR="${ERROR}\n - \$CATTLE_CONFIG_URL is empty"
[ "$ERROR" != "" ] && fail "$ERROR"

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


# start.

# first, run consul-template
rm -f haproxy.pid *.log
touch haproxy.pid

# here, consul must be just the host name, witOUT scheme, but WITH port.
# imPORTant, haha. (stupid fuck)
echo STARTUP starting consul-template
nohup ./consul-template -wait 5s:10s -consul $CONSUL_ADDRESS:8500 -config ./consul-template.cfg >> consul-template.log 2>&1 &

# we try to do this: http://engineeringblog.yelp.com/2015/04/true-zero-downtime-haproxy-reloads.html
waitfor haproxy.cfg
echo STARTUP restarting haproxy
./restart_haproxy.sh

# here, consul must be a real url with scheme.
echo STARTUP starting rancon
nohup rancon rancher consul -c -s url=$CATTLE_CONFIG_URL -b url=http://$CONSUL_ADDRESS >> rancon.log 2>&1 &

# do NOT fail on first non-zero output any longer
set +e

echo STARTUP starting tail
waitfor haproxy.log
waitfor rancon.log
waitfor consul-template.log
exec tail -n 100 -f *.log || true
 
killall -9 consul-template || true
killall -9 haproxy || true
killall -9 rancon || true
