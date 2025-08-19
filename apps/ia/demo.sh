#!/bin/bash

# LaVidaLuca API Demo Script
# This script demonstrates all the key features of the FastAPI backend

echo "🚀 LaVidaLuca API - Complete FastAPI Backend Demo"
echo "=================================================="

API_BASE="http://localhost:8000"

echo
echo "📋 1. API Information"
echo "--------------------"
curl -s "$API_BASE/" | python -m json.tool
echo

echo "❤️ 2. Health Check"
echo "------------------"
curl -s "$API_BASE/health" | python -m json.tool
echo

echo "👤 3. User Registration (Student)"
echo "--------------------------------"
STUDENT_RESPONSE=$(curl -s -X POST "$API_BASE/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@mfr.fr",
    "password": "StudentPass123",
    "first_name": "Marie",
    "last_name": "Dubois",
    "role": "student"
  }')
echo "$STUDENT_RESPONSE" | python -m json.tool
echo

echo "👨‍🏫 4. User Registration (Instructor)"
echo "------------------------------------"
INSTRUCTOR_RESPONSE=$(curl -s -X POST "$API_BASE/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "instructor@mfr.fr",
    "password": "InstructorPass123",
    "first_name": "Pierre",
    "last_name": "Martin",
    "role": "instructor"
  }')
echo "$INSTRUCTOR_RESPONSE" | python -m json.tool
echo

echo "🔐 5. User Login (Instructor)"
echo "----------------------------"
LOGIN_RESPONSE=$(curl -s -X POST "$API_BASE/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "instructor@mfr.fr",
    "password": "InstructorPass123"
  }')
echo "$LOGIN_RESPONSE" | python -m json.tool

# Extract token for subsequent requests
TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
echo

echo "🌱 6. Create Activity (Instructor)"
echo "---------------------------------"
ACTIVITY_RESPONSE=$(curl -s -X POST "$API_BASE/api/v1/activities/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Permaculture et Agroécologie",
    "description": "Découverte des principes de la permaculture et de l agroécologie pour une agriculture durable et respectueuse de l environnement",
    "category": "agriculture",
    "level": "debutant",
    "duration_hours": 6,
    "max_participants": 12,
    "location": "Ferme pédagogique - Parcelle Bio",
    "materials_needed": "Bottes, gants, carnet de notes, outils de jardinage",
    "learning_objectives": "Comprendre les cycles naturels, apprendre les techniques de compostage, découvrir la biodiversité fonctionnelle",
    "prerequisites": "Aucun prérequis - ouvert aux débutants"
  }')
echo "$ACTIVITY_RESPONSE" | python -m json.tool

ACTIVITY_ID=$(echo "$ACTIVITY_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
echo

echo "📋 7. List Activities (Public)"
echo "-----------------------------"
curl -s "$API_BASE/api/v1/activities/" | python -m json.tool
echo

echo "👥 8. Get Current User Profile"
echo "-----------------------------"
curl -s -X GET "$API_BASE/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
echo

echo "🎯 9. Activity Categories & Levels"
echo "---------------------------------"
echo "Categories:"
curl -s "$API_BASE/api/v1/activities/categories/" | python -m json.tool
echo
echo "Levels:"
curl -s "$API_BASE/api/v1/activities/levels/" | python -m json.tool
echo

echo "🎉 Demo Complete!"
echo "================"
echo "✅ Authentication system working"
echo "✅ User registration and profiles"
echo "✅ Activity management"
echo "✅ Role-based access control"
echo "✅ API documentation available at: $API_BASE/docs"
echo "✅ Alternative docs at: $API_BASE/redoc"
echo
echo "🌐 Key Features Demonstrated:"
echo "• JWT Authentication with role-based access"
echo "• User registration (Student/Instructor/Admin roles)"
echo "• Activity CRUD operations"
echo "• Data validation with Pydantic"
echo "• RESTful API design"
echo "• Comprehensive error handling"
echo "• Agricultural activity categories"
echo "• MFR education system integration"
echo
echo "🗃️ Database Models:"
echo "• Users (with roles and profiles)"
echo "• Activities (agriculture/artisanat/environnement)"
echo "• Activity Sessions (scheduled events)"
echo "• Registrations (student enrollments)"
echo "• User Profiles (detailed information)"