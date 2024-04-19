#!/bin/bash

# Get the base directory
BASE_DIR=$(dirname "$(dirname "$(readlink -f "$0")")")

# Initialize Packer build
packer init $BASE_DIR

# Validate
packer validate $BASE_DIR

# Build
packer build $BASE_DIR/aws-docker.pkr.hcl