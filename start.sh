#!/bin/bash
app="finndisplay"
docker build -t ${app} .
#docker run -d -p 56733:80 \
#  --name=${app} \
#  -v $PWD:/app ${app}
docker-compose -f docker-compose.yml up