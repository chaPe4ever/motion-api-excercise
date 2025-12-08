# PostgreSQL Schema Setup for Shared Database

This project uses PostgreSQL schemas to isolate tables when sharing a database with other projects (useful for free tier limitations).

## How It Works

1. **Schema Creation**: A migration (`motion/migrations/0001_create_schema.py`) creates a PostgreSQL schema named `motion` (configurable via `DB_SCHEMA` environment variable).

2. **Search Path**: The database connection is configured to use `search_path=motion,public`, which means:
   - New tables are created in the `motion` schema
   - Queries look in `motion` first, then `public` (for backward compatibility)

3. **Isolation**: Each project using the same database can have its own schema, preventing table name conflicts and migration issues.

## Configuration

Set the `DB_SCHEMA` environment variable in your production environment (Render, etc.):

```bash
DB_SCHEMA=motion
```

If not set, it defaults to `"motion"`.

## Migration Order

The schema creation migration runs automatically when you deploy. Since it has no dependencies, it will run before other migrations.

## Existing Tables

If you have existing tables in the `public` schema:
- They will still be accessible (because `public` is in the search_path)
- New tables will be created in the `motion` schema
- The migration to add the `created` field will work on tables in either schema

## Local Development

In local development with SQLite, the schema migration is skipped (schemas are PostgreSQL-specific). This is fine - SQLite doesn't need schema isolation.

## Deployment Steps

1. Set the `DB_SCHEMA` environment variable in your production environment
2. Deploy the code - migrations will run automatically via the `release` command in `Procfile`
3. The schema will be created and all tables will be isolated in that schema

## Benefits

- ✅ No table name conflicts with other projects
- ✅ Isolated migration history per project
- ✅ Can share a single PostgreSQL database across multiple projects
- ✅ Backward compatible (searches both schemas)

