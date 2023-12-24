import os
from sqlalchemy import URL
from sqlmodel import create_engine
from tables import create_tables
import time

# Class to store engine for all sessions

# Uncomment this block eventually!!!
# env_vars = os.environ
# DB_HOST = env_vars["DB_HOST"]
# DB_PASS = env_vars["DB_PASS"]
# DB_PORT = int(env_vars["DB_PORT"])

# engine_url = URL.create(
#     "postgresql",
#     username="postgres",
#     password=DB_PASS,
#     host=DB_HOST,
#     port=DB_PORT,
#     database="postgres"
# )

# Connect to POSTGRES db
engine_url = URL.create(
    "postgresql",
    username="postgres",
    password="abc",
    host="localhost",
    port=5432,
    database="postgres"
)

time.sleep(10)
engine = create_engine(engine_url, echo=True)
create_tables(engine)