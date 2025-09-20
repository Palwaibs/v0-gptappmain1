#!/bin/bash

echo "🏥 QUICK HEALTH CHECK"
echo "===================="

# Check if backend is responding
echo "Testing backend health..."
curl -s -o /dev/null -w "Backend Health: %{http_code}\n" https://api.aksesgptmurah.tech/health

# Check if frontend is accessible
echo "Testing frontend accessibility..."
curl -s -o /dev/null -w "Frontend: %{http_code}\n" https://aksesgptmurah.tech

# Check API endpoints
echo "Testing API endpoints..."
curl -s -o /dev/null -w "Packages API: %{http_code}\n" https://api.aksesgptmurah.tech/api/packages

echo ""
echo "Run 'python scripts/comprehensive_go_live_test.py' for detailed analysis"
