#!/bin/bash

echo "🚀 STARTING GO-LIVE READINESS TESTS"
echo "=================================="

# Set environment variables
export API_URL="https://api.aksesgptmurah.tech"
export FRONTEND_URL="https://aksesgptmurah.tech"

# Run main test suite
echo "Running comprehensive test suite..."
python3 scripts/test_go_live_readiness.py

echo ""
echo "Running payment flow tests..."
python3 scripts/test_payment_flow.py

echo ""
echo "🏁 ALL TESTS COMPLETED"
echo "Check go_live_test_results.json for detailed results"
