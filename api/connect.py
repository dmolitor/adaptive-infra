import os
from sqlalchemy import URL
from sqlmodel import create_engine
from db import create_tables

"""
This script connects to the Postgres database and creates the tables
initialized in `tables.py`
"""

env_vars = os.environ

ADAPTIVE_TESTING = env_vars.get("ADAPTIVE_TESTING")
DB_PASS = env_vars["POSTGRES_PASSWORD"]
DB_PORT = int(env_vars["POSTGRES_HOST_PORT"])
DB_USER = env_vars["POSTGRES_USER"]

# Creat the db URL and connect via SQLAlchemy/SQLModel
if ADAPTIVE_TESTING is not None and ADAPTIVE_TESTING:
    network = "localhost"
else:
    network = "database"

url = URL.create(
    "postgresql",
    username=DB_USER,
    password=DB_PASS,
    host=network,
    port=DB_PORT,
    database=DB_USER,
)
engine = create_engine(url, echo=False)

# Create the tables initialized in tables.py
create_tables(engine)
