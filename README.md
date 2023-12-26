# adaptive-infra
Infrastructure for adaptive learning with surveys and experiments.

## Requirements
[Install Docker and Docker Compose](https://docs.docker.com/compose/install/).

## Components
The following Docker Compose services:

- app:
    This service builds and hosts the front-end survey form. See
    `/ui` for corresponding code.

- api:
    This service builds and hosts the API that handles all interactions
    between the survey form and the database on the backend. See `/api`
    for corresponding code.

- database:
    This service utilizes the official PostgreSQL Docker image to store
    all relevant data and user resopnses.

## Running
To start the services run:
```shell
docker compose up -d
```

The app is now accessible at http://localhost:8000.

To shut everything down run:
```shell
docker compose down
```