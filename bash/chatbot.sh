#!/bin/bash
# This bash script builds the chatbot image based on docker/Dockerfile.spacy
# If the chatbot/spacy:latest docker image is missing, this will build it
echo "Building chatbot/spacy:latest image..."
docker build -t chatbot/spacy:latest -f docker/Dockerfile.spacy .