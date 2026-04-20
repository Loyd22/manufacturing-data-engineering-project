"""
This file is responsible for reading data from PostgreSQL.

Why we separate it:
- So database logic is not mixed with dashboard UI
- Other dashboard pages can reuse the same functions
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Load environment variables from the project root .env file
load_dotenv()


def get_database_url() -> str:
    """
    Build the PostgreSQL connection string from .env values.
    """
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def get_engine():
    """
    Create a SQLAlchemy engine.
    This is what Python uses to talk to PostgreSQL.
    """
    return create_engine(get_database_url())


def load_table(table_name: str) -> pd.DataFrame:
    """
    Read a full marts table into a pandas DataFrame.

    Example:
    load_table("marts.mart_daily_production_summary")
    """
    engine = get_engine()

    query = text(f"SELECT * FROM {table_name}")

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    return df