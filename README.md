# adaptive-infra
Infrastructure for adaptive learning with surveys and experiments.

## Requirements
[Install Docker and Docker Compose](https://docs.docker.com/compose/install/).

## Running
To start the services run:
```shell
docker compose --env-file compose.env up -d
```

The app is now accessible at http://localhost:8000.

To shut everything down run:
```shell
ocker compose --env-file compose.env down
```