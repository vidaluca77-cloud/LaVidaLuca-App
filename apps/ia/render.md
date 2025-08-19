# Render Deployment Configuration
# This file contains instructions for deploying the FastAPI backend on Render

## Build Command
pip install -r requirements.txt

## Start Command
uvicorn main:app --host 0.0.0.0 --port $PORT

## Environment Variables to Set in Render Dashboard:
# DEBUG=false
# SUPABASE_URL=your_supabase_url
# SUPABASE_ANON_KEY=your_supabase_anon_key  
# SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
# JWT_SECRET_KEY=your_super_secret_jwt_key_change_this_in_production
# ALLOWED_ORIGINS=["https://la-vida-luca.vercel.app"]

## Python Version
# Use Python 3.12 in Render settings