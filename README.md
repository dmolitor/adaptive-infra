# adaptive-infra
Infrastructure for adaptive learning with surveys and experiments.

## Requirements
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
    - [Configure the Cli for SSO](https://docs.aws.amazon.com/cli/latest/userguide/sso-configure-profile-token.html#sso-configure-profile-token-auto-sso)
- [just](https://github.com/casey/just)
- [Packer](https://developer.hashicorp.com/packer)
- [Python](https://www.python.org/downloads/)

### For local development

- [Docker Desktop](https://docs.docker.com/desktop/).

## Running locally
To get the stack running locally, it's as simple as:

```shell
docker compose up -d
```

To run using [Compose Watch](https://docs.docker.com/compose/file-watch/):
```shell
docker compose watch
```

To shut everything down:
```shell
docker compose down
```

## Services
The application is comprised of the following services:

- **app**:
    This service builds and hosts the front-end survey form. See
    `/ui` for corresponding code.

- **api**:
    This service builds and hosts the API that handles all interactions
    between the survey form and the database on the backend. See `/api`
    for corresponding code.

- **database**:
    This service utilizes the official PostgreSQL Docker image to store
    all relevant data and user responses.

## Build/Deploy

This project uses [just](https://github.com/casey/just) to organize building/deployment
commands. To see all available recipes run `just` in the root directory.
```shell
>> just
just --list
Available recipes:
    aws-ami-build         # Build AWS EC2 AMI with HCL Packer
    aws-security-group    # Provision an AWS security group
    aws-sso-configure     # Configure AWS SSO
    aws-sso-login profile="default" # AWS SSO login
    aws-swarm-launch      # Launch a Docker Swarm on an AWS EC2 server
    aws-swarm-terminate   # Terminate any active Docker Swarm AWS server
    aws-volume            # Provision an AWS EBS volume
    black                 # Format with Black
    check-aws             # Check if AWS CLI is installed
    check-dependencies    # Check all deploy dependencies
    check-docker          # Check if Docker is installed
    check-just            # Check if just is installed
    check-packer          # Check if HCL Packer is installed
    check-python          # Check if Python is installed
    default               # List all available recipes
    deploy                # Deploy the application to an AWS-hosted server
    docker-build-and-push # Build the app and api Docker images
    prolific-studies      # List all Prolific studies in the Adaptive Conjoint project
    terminate             # Terminate the running application and corresponding AWS server.
    track-swarm-logs ip key service="api" # Track the Docker swarm logs
    venv                  # Activate virtual environment and install Python dependencies
To execute a recipe: just [recipe-name]
```


### Build Docker images

To build the base Docker images and push them to DockerHub:
```shell
just docker-build-and-push
```

### Adaptive experiment

To deploy the adaptive experiment to an AWS server:
```shell
just deploy
```

To terminate the running AWS server:
```shell
just terminate
```
