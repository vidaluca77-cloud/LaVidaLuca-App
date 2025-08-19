from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
import os
import time
from dotenv import load_dotenv
from monitoring import metrics, health_check

# Load environment variables
load_dotenv()

app = FastAPI(
    title="La Vida Luca API",
    description="API pour le projet La Vida Luca - formation des jeunes en MFR",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monitoring middleware
@app.middleware("http")
async def add_monitoring(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        metrics.record_api_call(
            path=request.url.path,
            method=request.method,
            duration=duration,
            status_code=response.status_code
        )
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        metrics.record_error(e, {
            "path": request.url.path,
            "method": request.method,
            "duration": duration
        })
        raise

# Security
security = HTTPBearer()

# Models
class User(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None

class Activity(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    duration: Optional[int] = None
    category: str
    user_id: Optional[str] = None

# Health check endpoint
@app.get("/health")
async def health_check_endpoint():
    db_health = health_check.check_database()
    services_health = health_check.check_external_services()
    
    overall_healthy = (
        db_health["status"] == "healthy" and 
        services_health["overall_status"] == "healthy"
    )
    
    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "service": "La Vida Luca API",
        "database": db_health,
        "external_services": services_health
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "La Vida Luca API",
        "description": "API pour le projet La Vida Luca - formation des jeunes en MFR"
    }

# Users endpoints
@app.get("/users", response_model=List[User])
async def get_users():
    # TODO: Implement database query
    return []

# Activities endpoints  
@app.get("/activities", response_model=List[Activity])
async def get_activities():
    # TODO: Implement database query
    return []

@app.get("/activities/{activity_id}", response_model=Activity)
async def get_activity(activity_id: str):
    # TODO: Implement database query
    raise HTTPException(status_code=404, detail="Activity not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)