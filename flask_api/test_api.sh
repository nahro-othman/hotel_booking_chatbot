#!/bin/bash

# API Testing Script
# This script tests all the Flask API endpoints

echo "======================================================"
echo "🧪 Testing Hotel Booking Chatbot API"
echo "======================================================"
echo ""

API_URL="http://localhost:5001"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test health endpoint
echo -e "${BLUE}1. Testing Health Check...${NC}"
curl -s "$API_URL/health" | python -m json.tool
echo -e "\n"

# Test new session
echo -e "${BLUE}2. Creating New Session...${NC}"
SESSION_RESPONSE=$(curl -s -X POST "$API_URL/session/new")
echo "$SESSION_RESPONSE" | python -m json.tool
SENDER_ID=$(echo "$SESSION_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['sender'])" 2>/dev/null || echo "test-123")
echo -e "${GREEN}Session ID: $SENDER_ID${NC}"
echo -e "\n"

# Test chat - greeting
echo -e "${BLUE}3. Sending Message: 'hi'${NC}"
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"hi\", \"sender\": \"$SENDER_ID\"}" | python -m json.tool
echo -e "\n"

# Test chat - provide name
echo -e "${BLUE}4. Sending Message: 'John Doe'${NC}"
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"John Doe\", \"sender\": \"$SENDER_ID\"}" | python -m json.tool
echo -e "\n"

# Test active sessions
echo -e "${BLUE}5. Checking Active Sessions...${NC}"
curl -s "$API_URL/session/active" | python -m json.tool
echo -e "\n"

# Test bookings
echo -e "${BLUE}6. Getting All Bookings...${NC}"
curl -s "$API_URL/bookings" | python -m json.tool | head -20
echo -e "\n"

# Test documentation
echo -e "${BLUE}7. Getting API Documentation...${NC}"
curl -s "$API_URL/docs" | python -m json.tool | head -30
echo -e "\n"

# Test session reset
echo -e "${BLUE}8. Resetting Session...${NC}"
curl -s -X POST "$API_URL/session/reset" \
  -H "Content-Type: application/json" \
  -d "{\"sender\": \"$SENDER_ID\"}" | python -m json.tool
echo -e "\n"

echo -e "${GREEN}✅ All API tests completed!${NC}"
echo ""
echo "======================================================"
echo "🌐 Frontend: $API_URL"
echo "📚 API Documentation: $API_URL/docs"
echo "💚 Health Check: $API_URL/health"
echo "======================================================"

