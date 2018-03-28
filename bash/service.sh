#!/bin/bash
SERVICEBASE=$(docker images service_base:latest -q)

if [ "$SERVICEBASE" == "" ] ; then
    echo "service_base:latest docker image not found..."
    docker build -t service_base:latest -f docker/Dockerfile.servicebase .
fi

NAME="botnet"
docker rename $NAME $NAME-old
echo "Building docker image..."
docker build -t bot -f docker/Dockerfile.service .
echo "Create $NAME container..."
docker create --name $NAME -p 5000:5000 bot
echo "Stop old container"
docker stop $NAME-old
docker rm $NAME-old
echo "Start new container..."
docker start $NAME
echo "Add new container to network..."
    NET=$(docker network inspect botnet)
    if [ "$NET" == "[]" ] ; then
        docker network create botnet
    fi
docker network connect botnet $NAME
echo "Cleanup docker..."
docker container prune --force
docker volume prune --force
docker image prune --force