#!/bin/bash

sudo docker run -ti -d -p 27017:27017 -v $(pwd)/db:/data/db --name SmartHome_Database mongo
