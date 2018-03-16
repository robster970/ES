#!/bin/bash

docker pull robster970/sierra-nginx:latest
CONTAINER_ID=$(docker ps -a | grep -v Exit | grep 'robster970/sierra-nginx:latest' |awk '{print $1}')
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
docker run -p 80:5000 -d --restart=always -t robster970/sierra-nginx:latest
