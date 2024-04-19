#!/bin/bash

set -x

# Clone the adaptive-infra repo
sudo git clone https://github.com/dmolitor/adaptive-infra
cd adaptive-infra

# Initialize a one-node swarm
sudo docker swarm init

# Deploy the stack
sudo docker stack deploy -c ./docker-stack.yml adaptive_stack

echo "Waiting for services to be up..."
while true; do
    SERVICES_READY=true
    for service in $(sudo docker service ls --format "{{.Name}}"); do
        if ! sudo docker service ps "$service" --format "{{.CurrentState}}" | grep -q "Running"; then
            SERVICES_READY=false
            break
        fi
    done
    if [ "$SERVICES_READY" = true ]; then
        echo "All services are up"
        break
    else
        sleep 3
    fi
done

# Scale up the app service
sudo docker service scale adaptive_stack_app=20
