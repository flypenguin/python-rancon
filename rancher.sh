#!/usr/bin/env bash

# use this script for the rancher catalog service

ADD_PARAMS=""

if [ ! -z "$CATTLE_URL" ]; then
    echo "STARTUP: Detected CATTLE_URL: $CATTLE_URL"
    ADD_PARAMS="-s url=$CATTLE_URL"
    # we just assume we have rancher metadata access
    ENV_NAME=$(curl http://rancher-metadata/latest/self/stack/environment_name 2>/dev/null)
    if [ "$?" == "0" ]; then
        echo "STARTUP: Found environment '$ENV_NAME'"
        ADD_PARAMS=" $ADD_PARAMS -b cleanup_id='$ENV_NAME'"
    fi
fi

if [ ! -z "$CATTLE_ACCESS_KEY" -a ! -z "$CATTLE_SECRET_KEY" ]; then
    echo "STARTUP: Detected login credentials"
    ADD_PARAMS="$ADD_PARAMS -s accesskey=$CATTLE_ACCESS_KEY -s secretkey=$CATTLE_SECRET_KEY"
fi

exec python -um rancon -c -w10 rancher consul $ADD_PARAMS $@
