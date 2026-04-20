"""
Tests for database utility helpers.

What we are testing:
- database URL creation from environment variables
"""

from backend.utils.db import get_database_url


def test_get_database_url_contains_postgres_prefix():
    """
    This test checks that the database URL looks like a PostgreSQL connection string.
    """
    db_url = get_database_url()

    assert db_url.startswith("postgresql+psycopg2://")