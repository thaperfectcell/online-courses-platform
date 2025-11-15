#!/bin/sh

echo "Waiting for database and applying migrations..."

# Пытаемся применить миграции, пока не получится (например, БД ещё не готова)
until python manage.py migrate --noinput; do
  echo "Migration failed (maybe DB is not ready yet). Retrying in 3 seconds..."
  sleep 3
done

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Starting application..."
exec "$@"
