#!/bin/bash

# Login with Dockerhub credentials
docker login

# Build Docker images
docker compose build

# Push images
docker compose push