#!/bin/bash

# Get the base directory
BASE_DIR=$(dirname "$(dirname "$(readlink -f "$0")")")

# Initialize a one-node swarm
docker swarm init

# Deploy the stack
docker stack deploy -c $BASE_DIR/docker-stack.yml adaptive_stack

echo "Waiting for services to be up..."
while true; do
    SERVICES_READY=true
    for service in $(docker service ls --format "{{.Name}}"); do
        if ! docker service ps "$service" --format "{{.CurrentState}}" | grep -q "Running"; then
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
docker service scale adaptive_stack_app=20
