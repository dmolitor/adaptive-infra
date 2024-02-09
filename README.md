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

## Deploying on Docker
To start the services run:
```shell
docker compose up -d
```

The app is now accessible at http://localhost:8000.

To shut everything down run:
```shell
docker compose down
```

## Local Development

### Install dependencies
Set up and activate Python virtual environment and install requirements:
```
pip install -r ./api/requirements.txt
pip install -r ./ui/requirements.txt
```

### Run Postgres
To set up a Postgres db locally run the following in terminal:
```
export POSTGRES_PASSWORD=******
export POSTGRES_USER=******
docker run --name local-postgres -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_USER=$POSTGRES_USER -p 5432:5432 -d postgres
```

To test that the connection is valid:
```
docker exec local-postgres pg_isready -h localhost -p 5432 -U postgres
```

### Run API
Set the following environment variables:
```
export PYTHONPATH=$(pwd)/api
export ADAPTIVE_TESTING=true
export POSTGRES_HOST_PORT=5432
```

Then set up the API with:
```
uvicorn api.main:api --port 8000 --reload
```

Confirm you can access the API by running:
```
python -c "import requests as req; print(req.get('http://127.0.0.1:8000').text)"
```

### Run UI
Set the following environment variables:
```
export PYTHONPATH=$(pwd)/ui
export ADAPTIVE_TESTING=true
export API_HOST_PORT=8000
```

Then run the frontend with:
```
uvicorn ui.app:app --port 8080 --reload
```

Should be accessible at http://127.0.0.1:8080!

### Shut down Postgres database
Shut down the Postgres db with `docker rm local-postgres -f`.