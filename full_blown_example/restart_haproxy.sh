#!/usr/bin/bash
touch haproxy.pid
nohup haproxy -D -f ./haproxy.cfg -p ./haproxy.pid -sf $(cat ./haproxy.pid) >> haproxy.log 2>&1 &
