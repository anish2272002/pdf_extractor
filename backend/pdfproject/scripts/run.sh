#!/bin/sh
set -e

# Collect static files
echo "Collecting static files..."
python /pdfproject/manage.py collectstatic --noinput --clear

# Make migrations
echo "Making migrations..."
python /pdfproject/manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python /pdfproject/manage.py migrate

# Run Gunicorn with SSL
echo "Starting Gunicorn..."
gunicorn pdfproject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120