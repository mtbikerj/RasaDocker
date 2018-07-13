#!/bin/bash
# This bash script pulls the lasted image for rasa/rasa_nlu:latest-bare
echo "Pulling rasa/rasa_nlu:latest-bare from Docker cloud.  This might take a few minutes..."
docker image pull rasa/rasa_nlu:latest-bare