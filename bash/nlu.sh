#!/bin/bash
# This bash script rebuilds the NLU container
NAME=nlu
docker rename $NAME $NAME-old
echo "Building nlu:latest docker image"
docker build -t nlu:latest -f docker/Dockerfile.nlu .
echo "Starting nlu docker container"
docker run -d -p 5000:5000 -v /nlu/logs:/app/logs --name nlu nlu:latest start --path agent_nlu/agent
echo "Waiting 2 seconds to give docker IP time to spin up"
sleep 2
echo "Running curl against NLU to load model into memory"
echo "This will take a couple minutes..."
curl "http://localhost:5000/parse?q=hello&model=default"
echo "Stopping and removing old container"
docker stop $NAME-old
docker rm $NAME-old
echo "Docker cleanup..."
docker container prune --force
docker volume prune --force
docker image prune --force
