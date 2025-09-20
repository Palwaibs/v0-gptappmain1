#!/bin/bash

echo "🔧 FIXING 502 BAD GATEWAY ERRORS"
echo "================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
if ! command_exists docker; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Step 1: Check environment file
echo "1️⃣ Checking environment configuration..."
if [ ! -f "backend/.env" ]; then
    echo "⚠️ backend/.env not found. Creating from template..."
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo "✅ Created backend/.env from template"
        echo "🚨 IMPORTANT: Edit backend/.env with your actual values!"
    else
        echo "❌ No .env.example found. Please create backend/.env manually."
    fi
fi

# Step 2: Stop all services
echo "2️⃣ Stopping all services..."
docker-compose down

# Step 3: Remove old containers and images
echo "3️⃣ Cleaning up old containers..."
docker-compose rm -f
docker system prune -f

# Step 4: Rebuild backend
echo "4️⃣ Rebuilding backend container..."
docker-compose build --no-cache backend

# Step 5: Start database first
echo "5️⃣ Starting database services..."
docker-compose up -d postgres redis

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Step 6: Start backend
echo "6️⃣ Starting backend service..."
docker-compose up -d backend

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 15

# Step 7: Test health endpoint
echo "7️⃣ Testing backend health..."
if curl -f http://localhost:5000/health >/dev/null 2>&1; then
    echo "✅ Backend health check passed!"
else
    echo "❌ Backend health check failed. Checking logs..."
    docker-compose logs --tail=20 backend
fi

# Step 8: Start remaining services
echo "8️⃣ Starting all services..."
docker-compose up -d

echo ""
echo "🏁 FIX ATTEMPT COMPLETE"
echo "======================"
echo "Run the following to check status:"
echo "  docker-compose ps"
echo "  curl http://localhost:5000/health"
echo ""
echo "If issues persist, check logs with:"
echo "  docker-compose logs backend"
