# database

This directory is used for persisting PostgreSQL data. In the `docker-compose.yml`
file, this directory is mounted to the PostgreSQL default data directory:
```yaml
    environment:
      PGDATA=/var/lib/postgresql/data/pgdata

    volumes:
      - ./database:/var/lib/postgresql/data
```

Note: setting the `PGDATA` environment variable is **essential** since, in this
case we're mounting a local directory that isn't owned by user `postgres`.
For a better explanation, see the [Environment Variables > `PGDATA`](https://hub.docker.com/_/postgres)
section of the Docker docs.