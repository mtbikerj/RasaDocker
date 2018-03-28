#!/bin/bash
# This bash script rebuilds the NLU container
NAME=nlu
docker rename $NAME $NAME-old
echo "Building nlu:latest docker image"
docker build -t nlu:latest -f docker/Dockerfile.nlu .
echo "Starting nlu docker container"
docker run -d -v /nlu/logs:/app/logs --name nlu nlu:latest start
echo "Add new container to network botnet"
NET=$(docker network inspect botnet)
if [ "$NET" == "[]" ] ; then
    docker network create botnet
fi
docker network connect botnet $NAME
echo "Waiting 2 seconds to give docker IP time to spin up"
sleep 2
NLU_LOCAL=$(docker inspect --format "{{ .NetworkSettings.Networks.botnet.IPAddress }}" "$NAME")
echo "Running curl against NLU internal IP $NLU_LOCAL:5000 to load model into memory"
echo "This will take a couple minutes..."
curl "http://$NLU_LOCAL:5000/parse?q=hello&model=default"
echo "Stopping and removing old container"
docker stop $NAME-old
docker rm $NAME-old
echo "Docker cleanup..."
docker container prune --force
docker volume prune --force
docker image prune --force
