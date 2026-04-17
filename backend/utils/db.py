"""
This file is responsible for creating the database connection.

Why we separate this:
- So connection logic is not mixed with ingestion logic
- Other parts of the project can reuse this later
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load values from the .env file
load_dotenv()


def get_database_url() -> str:
    """
    Build the PostgreSQL connection URL from environment variables.
    """
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def get_engine():
    """
    Create and return a SQLAlchemy engine.

    The engine is what Python uses to talk to PostgreSQL.
    """
    database_url = get_database_url()
    return create_engine(database_url)