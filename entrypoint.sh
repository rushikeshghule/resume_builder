#!/bin/bash
set -e

# Set default port if not provided
export PORT=${PORT:-8000}

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting server on port $PORT..."
# Use exec to ensure gunicorn receives signals properly
exec gunicorn resumecraft.wsgi:application --bind 0.0.0.0:$PORT --workers=2 --threads=4 --timeout=120
