# Ensure PostgreSQL search_path is set for schema isolation
# This monkey-patches Django's database connection to set search_path immediately after connection
from decouple import config
from django.db.backends.postgresql.base import DatabaseWrapper

_original_get_new_connection = DatabaseWrapper.get_new_connection


def get_new_connection_with_search_path(self, conn_params):
    """Override to set search_path immediately after connection creation."""
    # Get the original connection
    conn = _original_get_new_connection(self, conn_params)

    # Set search_path if we're using PostgreSQL and have a schema configured
    db_schema = config("DB_SCHEMA", default="test")
    if db_schema and self.vendor == "postgresql":
        try:
            # For psycopg3, we need to ensure autocommit is enabled before executing
            # to avoid transaction conflicts with Django's connection management
            original_autocommit = None
            try:
                # Save original autocommit state
                if hasattr(conn, "autocommit"):
                    original_autocommit = conn.autocommit
                    # Enable autocommit temporarily to avoid transaction conflicts
                    conn.autocommit = True
            except Exception:
                # If we can't set autocommit, try to proceed anyway
                pass

            try:
                # First, ensure the schema exists (create if it doesn't)
                # This ensures the schema is available before migrations run
                with conn.cursor() as cursor:
                    cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{db_schema}";')
                    # Then set search_path to use the schema
                    cursor.execute(f'SET search_path TO "{db_schema}", public;')
            finally:
                # Restore original autocommit state if we changed it
                if original_autocommit is not None and hasattr(conn, "autocommit"):
                    try:
                        conn.autocommit = original_autocommit
                    except Exception:
                        pass
        except Exception as e:
            # If setting fails, log it but continue
            # The connection options in settings.py might handle it
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Could not set search_path via monkey-patch: {e}. "
                f"Relying on connection options in settings.py."
            )

    return conn


# Apply the monkey-patch
DatabaseWrapper.get_new_connection = get_new_connection_with_search_path
