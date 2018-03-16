#!/bin/bash

echo $SIERRA_ENV
docker pull robster970/sierra-nginx:latest
CONTAINER_ID=$(docker ps -a | grep -v Exit | grep 'sierra-nginx' |awk '{print $1}')
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
docker run -p 80:5000 -d --restart=always -t robster970/sierra-nginx:latest
docker ps -a