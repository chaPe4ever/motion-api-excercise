# Local Development Setup

This guide explains how to run the Motion API locally using Docker.

## Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

## Quick Start

**Note:** The `docker-compose.yml` file explicitly sets all environment variables for local development, so you don't need to modify your `.env` file. The local database URL is hardcoded in docker-compose.yml and will override any `DATABASE_URL` in your `.env` file.

1. **Start the services**:
   ```bash
   docker compose up -d
   ```

2. **Run migrations** (that's it - no schema setup needed!):
   ```bash
   docker compose exec backend python manage.py migrate
   ```

4. **Create a superuser** (optional):
   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

5. **Access the API**:
   - API: http://localhost:8000/
   - Swagger UI: http://localhost:8000/swagger/
   - ReDoc: http://localhost:8000/redoc/
   - Admin: http://localhost:8000/admin/

## Environment Variables

The `docker-compose.yml` file explicitly sets all environment variables for local development:

- `DEBUG=1` - Enables Django debug mode
- `ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0` - Allowed hosts for local access
- `DATABASE_URL=postgresql://motion_user:motion_password@db:5432/motion_db` - Local Docker database
- `DB_SCHEMA=` - Empty (uses default `public` schema)
- `SECURE_SSL_REDIRECT=false` - Disabled for local development

**Important:** These values are hardcoded in `docker-compose.yml` and will override any values in your `.env` file, so you don't need to modify `.env` for local development.

The `.env.local` file is provided as a reference template, but it's not required since docker-compose.yml sets everything explicitly.

## Common Commands

### Start services
```bash
docker compose up -d
```

### Stop services
```bash
docker compose down
```

### View logs
```bash
docker compose logs -f backend
```

### Run migrations
```bash
docker compose exec backend python manage.py migrate
```

### Create superuser
```bash
docker compose exec backend python manage.py createsuperuser
```

### Collect static files
```bash
docker compose exec backend python manage.py collectstatic --noinput
```

### Access Django shell
```bash
docker compose exec backend python manage.py shell
```

### Run tests
```bash
docker compose exec backend python manage.py test
```

### Rebuild after dependency changes
```bash
docker compose build backend
docker compose up -d
```

## Database Access

The PostgreSQL database is exposed on port `5432` for local access:

- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `motion_db` (or value from `POSTGRES_DB` in `.env`)
- **User**: `motion_user` (or value from `POSTGRES_USER` in `.env`)
- **Password**: `motion_password` (or value from `POSTGRES_PASSWORD` in `.env`)
- **Schema**: `public` (default PostgreSQL schema - no setup needed!)

You can connect using any PostgreSQL client (pgAdmin, DBeaver, psql, etc.).

## Code Changes

The `docker-compose.yml` mounts the current directory (`.`) to `/app` in the container, so code changes are reflected immediately when using Django's `runserver` (no rebuild needed).

## Troubleshooting

### Port already in use
If port 8000 or 5432 is already in use, change the ports in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

### Database connection errors
- Ensure the `db` service is healthy: `docker compose ps`
- Check database logs: `docker compose logs db`
- Verify environment variables in `.env`

### Static files not loading
Run collectstatic:
```bash
docker compose exec backend python manage.py collectstatic --noinput
```

### Need to reset database
```bash
docker compose down -v  # Removes volumes
docker compose up -d
docker compose exec backend python manage.py migrate
```

## Differences from Production

- Uses Django's `runserver` instead of gunicorn (auto-reload on code changes)
- Debug mode enabled (`DEBUG=True`)
- No SSL/HTTPS
- Database exposed on host port 5432
- Code mounted as volume (live editing)
- Uses default `public` schema (no custom schema needed for local development)
