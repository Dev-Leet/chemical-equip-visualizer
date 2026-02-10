#!/bin/bash
set -e

echo "Setting up Chemical Equipment Visualizer Backend..."

cd "$(dirname "$0")/../../backend"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "WARNING: Please update .env with production values!"
fi

mkdir -p logs media/uploads staticfiles

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser (skip if exists)..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete!"
echo "To run the server: python manage.py runserver"