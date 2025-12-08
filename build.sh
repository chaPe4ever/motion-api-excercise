#!/bin/bash
# Build script for Render deployment
# This ensures static files are collected during build

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install -r requirements-production.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"

