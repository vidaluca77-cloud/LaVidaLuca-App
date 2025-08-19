# FastAPI Backend for La Vida Luca

This is the FastAPI backend service for the La Vida Luca application.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

4. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Structure

- `app/` - Main application code
  - `api/` - API route handlers
  - `core/` - Core configurations and settings
  - `db/` - Database configuration and session management
  - `models/` - SQLAlchemy models
  - `schemas/` - Pydantic schemas for request/response
  - `services/` - Business logic services
  - `utils/` - Utility functions
- `tests/` - Test suite