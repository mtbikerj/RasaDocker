#!/bin/bash
AGENTS=$(ls agents)

for agent in $AGENTS; do
	echo "Building bot: $agent..."
	NAME=$agent
	docker rename $NAME $NAME-old
	echo "Create $NAME container..."
	docker stop $NAME-old
	docker container rm $NAME-old
	echo "Start new container"
	docker run -d -v $(pwd)/agents/$agent/models:/app/models -v $(pwd)/agents/$agent/config:/app/config --name $NAME rasa/rasa_core:latest start --core models/agent -c rest --endpoints config/endpoints.yml -u agent/default
	echo "Add new container to network botnet..."
	NET=$(docker network inspect botnet)
	if [ "$NET" == [] ] ; then
	    docker network create botnet
	fi
	docker network connect botnet $NAME
done
echo "Clean up docker"
docker container prune --force
docker volume prune --force
docker image prune --force
