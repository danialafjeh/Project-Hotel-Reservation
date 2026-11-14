#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

until python -c "
import os
import psycopg2

connection = psycopg2.connect(
    dbname=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['DB_HOST'],
    port=os.environ['DB_PORT']
)

connection.close()
"; do
    sleep 2
done

echo "PostgreSQL is ready."

echo "Applying database migrations..."

python manage.py migrate --noinput

echo "Loading initial database data..."

python manage.py shell -c "
from django.core.management import call_command
from main.models import HotelRoom

if not HotelRoom.objects.exists():
    call_command('loaddata', 'data/sample_data.json')
else:
    print('Initial data already exists. Skipping fixture loading.')
"

echo "Starting Django development server..."
echo "Open your browser at: http://localhost:8000"

python manage.py runserver 0.0.0.0:8000