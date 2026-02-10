#!/bin/bash
set -e

echo "Deploying Chemical Equipment Visualizer..."

cd "$(dirname "$0")/../.."

if [ ! -f "backend/.env" ]; then
    echo "ERROR: .env file not found. Please create it from .env.example"
    exit 1
fi

echo "Starting deployment with Docker Compose..."
cd deployment/docker

docker-compose down
docker-compose build
docker-compose up -d

echo "Waiting for services to start..."
sleep 10

echo "Running database migrations..."
docker-compose exec backend python manage.py migrate

echo "Collecting static files..."
docker-compose exec backend python manage.py collectstatic --noinput

echo "Deployment complete!"
echo "Backend available at: http://localhost:8000"
echo "Admin panel at: http://localhost:8000/admin"