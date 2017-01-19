#!/usr/bin/env bash

# use this script for the rancher catalog service

ADD_PARAMS=""

if [ ! -z "$CATTLE_URL" ]; then
    echo "STARTUP: "
    echo "    Detected CATTLE_URL: $CATTLE_URL"
    ADD_PARAMS="-s url=$CATTLE_URL"
    # we just assume we have rancher metadata access
    ENV_NAME=$(curl http://rancher-metadata/latest/self/stack/environment_name 2>/dev/null)
    if [ "$?" == "0" ]; then
        echo "    Found environment '$ENV_NAME'"
        CLEANUP0=$(echo $CATTLE_URL | sed -r 's%https?://%%g' | cut -d/ -f1 | tr '[[:upper:]]' '[[:lower:]]' | sed -r 's/[^A-Za-z0-9_-]/-/g')
        CLEANUP1=$(echo $ENV_NAME | tr '[[:upper:]]' '[[:lower:]]' | sed -r 's/[^A-Za-z0-9_-]/-/g')
        CLEANUP="${CLEANUP0}-${CLEANUP1}"
        echo "    Using cleanup ID  '$CLEANUP'"
        ADD_PARAMS=" $ADD_PARAMS -b cleanup_id=$CLEANUP"
    fi
fi

if [ ! -z "$CATTLE_ACCESS_KEY" -a ! -z "$CATTLE_SECRET_KEY" ]; then
    echo "    Detected login credentials"
    ADD_PARAMS="$ADD_PARAMS -s accesskey=$CATTLE_ACCESS_KEY -s secretkey=$CATTLE_SECRET_KEY"
fi

exec python -um rancon -c -w10 rancher consul $ADD_PARAMS $@
