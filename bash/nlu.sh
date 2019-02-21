#!/bin/bash
# This bash script rebuilds the NLU container
NAME=nlu
docker rename $NAME $NAME-old
echo "Starting nlu docker container"
docker run -d -p 5000:5000 -v $(~/rasa_logs/):/app/logs --name nlu rasa/rasa_nlu:latest-full
echo "Waiting 2 seconds to give docker IP time to spin up"
sleep 2
echo "Running curl to train the agent project and default model... this will take a few minutes"
curl --request POST --header 'content-type: application/x-yml' --data-binary @nlu/train_md.yml --url 'http://localhost:5000/train?project=agent&model=default'
echo "This will take a couple minutes..."
curl "http://localhost:5000/parse?q=hello&project=agent&model=default"
echo "Stopping and removing old container"
docker stop $NAME-old
docker rm $NAME-old
echo "Docker cleanup..."
docker container prune --force
docker volume prune --force
docker image prune --force
