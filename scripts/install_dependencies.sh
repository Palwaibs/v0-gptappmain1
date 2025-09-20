#!/bin/bash

echo "🔧 Installing Missing Dependencies for Go-Live Tests"
echo "=================================================="

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install Python pip first."
    exit 1
fi

# Install PyMySQL for database connectivity
echo "📦 Installing PyMySQL..."
pip install PyMySQL

# Install other test dependencies
echo "📦 Installing requests (if not already installed)..."
pip install requests

echo "✅ Dependencies installed successfully!"
echo ""
echo "Now you can run the comprehensive test:"
echo "python scripts/comprehensive_go_live_test.py"
