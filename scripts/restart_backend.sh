#!/bin/bash

echo "🔄 RESTARTING BACKEND WITH NEW ENVIRONMENT VARIABLES"
echo "============================================================"

# Stop existing services
echo "⏹️  Stopping existing services..."
docker-compose down

# Rebuild backend with new env
echo "🔨 Rebuilding backend container..."
docker-compose build backend

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait a moment for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if backend is running
echo "🏥 Checking backend health..."
curl -f https://api.aksesgptmurah.tech/health || echo "❌ Backend not responding yet"

echo "✅ Backend restart complete!"
echo "Run the test script again to verify: python scripts/test_go_live_readiness.py"
