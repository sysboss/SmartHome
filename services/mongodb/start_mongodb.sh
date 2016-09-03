#!/bin/bash

INSTANCE_NAME=SmartHome_Database
ROOT_DIR=/opt/SmartHome

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# check mongodb container state
IS_RUNNING=$(docker inspect -f {{.State.Running}} $INSTANCE_NAME 2>/dev/null)

# check if already running
if [[ $IS_RUNNING == "true" ]]; then
    echo MongoDB $INSTANCE_NAME is already running
    exit 1
fi

docker run -ti -d -p 27017:27017 -v $ROOT_DIR/services/mongodb/db:/data/db --name $INSTANCE_NAME mongo
