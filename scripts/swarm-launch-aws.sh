#!/bin/bash

# Clone the adaptive-infra repo
sudo git clone -b survey-update https://github.com/dmolitor/adaptive-infra
cd adaptive-infra

# Copy the correct .env file into the repo
sudo rm .env
sudo cp ../.env ./

# Load environment variables
set -a
source .env
set +a

# Deploy the stack
envsubst < docker-stack.yml | sudo docker stack deploy --detach=false -c - adaptive_stack
