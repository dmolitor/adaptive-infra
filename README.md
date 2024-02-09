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
    all relevant data and user responses.

## Running on Docker
To start the services run:
```shell
docker compose up -d
```

The app is now accessible at http://localhost:8000.

To shut everything down run:
```shell
docker compose down
```

## Running locally

To set up a Postgres db locally run the following in terminal:
```
docker run --name local-postgres -e POSTGRES_PASSWORD=abc -e POSTGRES_USER=adaptive-conjoint -p 5432:5432 -d postgres
```

To test that the connection is valid:
```
docker exec local-postgres pg_isready -h localhost -p 5432 -U adaptive-conjoint
```