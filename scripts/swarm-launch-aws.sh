#!/bin/bash

# Clone the adaptive-infra repo
sudo git clone https://github.com/dmolitor/adaptive-infra
cd adaptive-infra

# Load environment variables
set -a
source .env
set +a

# Initialize a one-node swarm
sudo docker swarm init

# Deploy the stack
envsubst < docker-stack.yml | sudo docker stack deploy --detach=false -c - adaptive_stack

# Scale up the app service
sudo docker service scale adaptive_stack_app=2
