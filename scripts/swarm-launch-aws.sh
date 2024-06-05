#!/bin/bash

# Clone the adaptive-infra repo
sudo git clone -b survey-update https://github.com/dmolitor/adaptive-infra
cd adaptive-infra

# Copy the correct .env file into the repo
sudo rm .env
sudo mv ../.env ./

# Load environment variables
set -a
source .env
set +a

# Initialize a one-node swarm
sudo docker swarm init

# Deploy the stack
envsubst < docker-stack.yml | sudo docker stack deploy --detach=false -c - adaptive_stack
