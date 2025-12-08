# Ensure PostgreSQL search_path is set for schema isolation
# This runs when Django initializes to set search_path on database connections
from decouple import config
from django.db.backends.postgresql.base import DatabaseWrapper

_original_get_new_connection = DatabaseWrapper.get_new_connection


def get_new_connection_with_search_path(self, conn_params):
    """Override to set search_path after connection is created."""
    conn = _original_get_new_connection(self, conn_params)
    db_schema = config("DB_SCHEMA", default="test")
    if db_schema:
        with conn.cursor() as cursor:
            cursor.execute(f'SET search_path TO "{db_schema}", public;')
    return conn


# Monkey-patch to ensure search_path is set on all new connections
DatabaseWrapper.get_new_connection = get_new_connection_with_search_path
