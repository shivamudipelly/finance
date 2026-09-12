#!/bin/bash

echo "=========================================="
echo "  Market AI Platform - One-Click Start"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed."
    echo "   Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose is not installed."
    echo "   Please install Docker Desktop (includes Compose)."
    exit 1
fi

echo "Docker is installed"
echo ""

# Stop any existing containers
echo "Stopping existing containers..."
docker compose down 2>/dev/null || true

# Build and start all services
echo "Building and starting all services..."
echo "   This includes: Database, Redis, AI Engine (Ollama), Backend, Frontend"
echo "   First run will download images and AI model (may take 5-10 minutes)"
echo ""

docker compose up --build -d

echo ""
echo "Waiting for services to start..."
sleep 15

# Check container status
echo ""
echo "Container Status:"
docker compose ps

echo ""
echo "=========================================="
echo "  Platform Started Successfully!"
echo "=========================================="
echo ""
echo "Access Points:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "AI Model:"
echo "   The AI engine (Ollama) is downloading the Llama 3.2 model."
echo "   This happens automatically on first run."
echo "   Chat features will work once model is ready (~2-5 min)."
echo ""
echo "Common Commands:"
echo "   ./start.sh              - Start everything"
echo "   ./stop.sh               - Stop everything"
echo "   ./logs.sh               - View logs"
echo "   docker compose down -v  - Reset all data"
echo ""
echo "Notes:"
echo "   - All data is stored in Docker volumes (persistent)"
echo "   - Uses FREE services only (no API keys needed)"
echo "   - Market data may use mock data if free APIs are rate-limited"
echo ""
