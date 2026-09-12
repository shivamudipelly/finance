#!/bin/bash

echo "=========================================="
echo "  Market AI - Personal Intelligence Platform"
echo "=========================================="
echo ""

# Start Docker containers
echo "Starting Docker containers (PostgreSQL + Redis)..."
cd /workspace
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 5

# Install backend dependencies
echo "Installing backend dependencies..."
cd /workspace/backend
pip install -r requirements.txt -q

# Run database migrations
echo "Running database migrations..."
python -m app.main &
sleep 3

# Start frontend
echo "Starting frontend development server..."
cd /workspace/frontend
npm run dev -- --host 0.0.0.0 &

echo ""
echo "=========================================="
echo "  Application Started!"
echo "=========================================="
echo ""
echo "Backend API:  http://localhost:8000"
echo "Frontend UI:  http://localhost:3000"
echo ""
echo "API Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

wait
