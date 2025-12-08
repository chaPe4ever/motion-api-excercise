#!/bin/bash
# Build script for Render deployment
# This ensures static files are collected and migrations are run during build

set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure

echo "Installing dependencies..."
pip install -r requirements-production.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "=========================================="
echo "Running database migrations..."
echo "=========================================="
python manage.py migrate --noinput --verbosity=2

echo "=========================================="
echo "Build complete!"
echo "=========================================="

