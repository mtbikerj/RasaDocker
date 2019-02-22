#!/bin/bash
# This bash script rebuilds the NLU container
NAME=nlu
docker rename $NAME $NAME-old
echo "Starting nlu docker container"
docker run -d -v $(pwd)/rasa_logs:/app/logs --name nlu rasa/rasa_nlu:latest-full
echo "Waiting 2 seconds to give docker IP time to spin up"
sleep 2
echo "Add new container to network botnet"
NET=$(docker network inspect botnet)
if [ "$NET" == "[]" ] ; then
    docker network create botnet
fi
docker network connect botnet $NAME
NLU_LOCAL=$(docker inspect --format "{{ .NetworkSettings.Networks.botnet.IPAddress }}" "$NAME")
echo "Running curl to train the agent project and default model... this will take a few minutes"
curl --request POST --header 'content-type: application/x-yml' --data-binary @nlu/train_md.yml --url 'http://$NLU_LOCAL:5000/train?project=agent&model=default'
echo "This will take a couple minutes..."
curl "http://$NLU_LOCAL:5000/parse?q=hello&project=agent&model=default"
echo "Stopping and removing old container"
docker stop $NAME-old
docker rm $NAME-old
echo "Docker cleanup..."
docker container prune --force
docker volume prune --force
docker image prune --force
