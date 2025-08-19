#!/bin/bash

# La Vida Luca Backend API Test Script
# This script demonstrates how to test the main API endpoints

BASE_URL="http://localhost:8000"
API_BASE="$BASE_URL/api/v1"

echo "🚀 Testing La Vida Luca Backend API"
echo "======================================"

# Test health endpoint
echo -e "\n📊 Testing health endpoint..."
curl -s "$BASE_URL/health" | jq '.'

# Test root endpoint
echo -e "\n🏠 Testing root endpoint..."
curl -s "$BASE_URL/" | jq '.'

# Register a test user
echo -e "\n👤 Registering test user..."
REGISTER_RESPONSE=$(curl -s -X POST "$API_BASE/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "testpassword123",
    "school": "MFR Test",
    "level": "debutant"
  }')

echo "$REGISTER_RESPONSE" | jq '.'

# Login with test user
echo -e "\n🔐 Logging in test user..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_BASE/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpassword123")

echo "$LOGIN_RESPONSE" | jq '.'

# Extract token
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')

if [ "$TOKEN" != "null" ] && [ "$TOKEN" != "" ]; then
    echo "✅ Login successful, token obtained"
    
    # Test authenticated endpoint
    echo -e "\n👤 Getting current user profile..."
    curl -s -X GET "$API_BASE/users/me" \
      -H "Authorization: Bearer $TOKEN" | jq '.'
    
    # Create an activity
    echo -e "\n📚 Creating test activity..."
    ACTIVITY_RESPONSE=$(curl -s -X POST "$API_BASE/activities/" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d '{
        "title": "Introduction à la permaculture",
        "description": "Découverte des principes de base de la permaculture et mise en pratique dans un potager pédagogique",
        "category": "agriculture",
        "difficulty": "debutant",
        "duration_hours": 4,
        "materials_needed": "Outils de jardinage, graines, plants",
        "prerequisites": "Aucun prérequis nécessaire",
        "learning_objectives": "Comprendre les principes de la permaculture et savoir créer un petit potager",
        "location_type": "outdoor",
        "max_participants": 15,
        "is_featured": true
      }')
    
    echo "$ACTIVITY_RESPONSE" | jq '.'
    
    # List activities
    echo -e "\n📚 Listing all activities..."
    curl -s "$API_BASE/activities/" | jq '.'
    
    # Get activity categories
    echo -e "\n🏷️ Getting activity categories..."
    curl -s "$API_BASE/activities/categories/" | jq '.'
    
    # Get activity difficulties
    echo -e "\n📊 Getting difficulty levels..."
    curl -s "$API_BASE/activities/difficulties/" | jq '.'
    
    # Test recommendations
    echo -e "\n🤖 Getting trending recommendations..."
    curl -s "$API_BASE/recommendations/trending/" | jq '.'
    
    # Test personalized recommendations (will likely fail due to fake OpenAI key)
    echo -e "\n🎯 Testing personalized recommendations..."
    RECOMMENDATIONS_RESPONSE=$(curl -s "$API_BASE/recommendations/" \
      -H "Authorization: Bearer $TOKEN")
    
    if echo "$RECOMMENDATIONS_RESPONSE" | jq -e '.detail' > /dev/null; then
        echo "❌ Personalized recommendations failed (expected with test OpenAI key)"
        echo "$RECOMMENDATIONS_RESPONSE" | jq '.detail'
    else
        echo "$RECOMMENDATIONS_RESPONSE" | jq '.'
    fi
    
else
    echo "❌ Login failed, cannot test authenticated endpoints"
fi

echo -e "\n✅ API testing completed!"
echo "💡 For interactive testing, visit: $BASE_URL/docs"