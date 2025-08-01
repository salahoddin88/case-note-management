#!/bin/bash
# Simple Docker test script for Case Note Management System

echo "🐳 Testing Docker Setup for Case Note Management System"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is installed and running"

# Build the image
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Run the container
echo "🚀 Starting container..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Container started successfully"
    echo "🌐 Application should be available at http://localhost:8000"
    echo "📚 API docs available at http://localhost:8000/api/docs"
    echo ""
    echo "To stop the container, run: docker-compose down"
    echo "To view logs, run: docker-compose logs -f"
else
    echo "❌ Failed to start container"
    exit 1
fi