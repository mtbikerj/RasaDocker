#!/bin/bash
BRANCH='master'
CORE=$(docker images rasa_core:latest -q)

if [ "$CORE" == "" ] ; then
	echo "rasa_core container not found.  Building..."
	docker build -t rasa_core:latest -f docker/Dockerfile.rasacore
fi

AGENTS=$(ls agents)

for agent in $AGENTS; do
	echo "Building bot: $agent..."
	NAME=$agent
	docker rename $NAME $NAME-old
	echo "Build docker container for $agent agent ..."
	docker build -t $agent:$BRANCH --build-arg AGENT=$agent -f docker/Dockerfile.agent .
	echo "Create $NAME container..."
	docker stop $NAME-old
	docker container rm $NAME-old
	echo "Start new container"
	docker run -d --name $NAME $NAME
	echo "Add new container to network botnet..."
    NET=$(docker network inspect botnet)
    if [ "$NET" == "[]" ] ; then
        docker network create botnet
    fi
    docker network connect botnet $NAME
done
echo "Clean up docker"
docker container prune --force
docker volume prune --force
docker image prune --force