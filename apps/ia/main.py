from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Literal
import os
from dotenv import load_dotenv
import openai
import logging

load_dotenv()

# Configuration
app = FastAPI(title="La Vida Luca API")
openai.api_key = os.getenv("OPENAI_API_KEY")

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models
class GuideRequest(BaseModel):
    question: str
    activity_title: Optional[str] = None
    safety_level: int = 1
    duration_min: int = 20
    materials: List[str] = []

class GuideResponse(BaseModel):
    title: str
    duration: str
    materials: List[str]
    rules: List[str]
    checklist: List[str]
    answer: Optional[str]
    question_echo: str

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

# Routes
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/guide")
async def get_guide(request: GuideRequest):
    if not openai.api_key:
        raise HTTPException(status_code=401, detail="OpenAI API key not configured")
    
    try:
        # Build prompt
        system_prompt = """Tu es une IA agricole experte qui aide à La Vida Luca.
        Sois prudent et pratique dans tes conseils.
        Réponds de manière structurée avec:
        - Des règles de sécurité
        - Une checklist pratique
        - Une réponse détaillée"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.question}
        ]

        response = openai.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-mini"),
            messages=messages,
            temperature=0.7,
        )

        # Parse response
        answer = response.choices[0].message.content

        # Default values if AI doesn't provide
        rules = [
            "Toujours suivre les consignes de sécurité",
            "Porter les équipements de protection",
            "Signaler tout problème"
        ]
        
        checklist = [
            "Vérifier le matériel",
            "S'assurer d'avoir l'équipement nécessaire",
            "Prendre connaissance des risques"
        ]

        return GuideResponse(
            title=request.activity_title or "Guide agricole",
            duration=f"{request.duration_min} minutes",
            materials=request.materials,
            rules=rules,
            checklist=checklist,
            answer=answer,
            question_echo=request.question
        )

    except Exception as e:
        logger.error(f"Error in /guide: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/chat")
async def chat(request: ChatRequest):
    if not openai.api_key:
        raise HTTPException(status_code=401, detail="OpenAI API key not configured")
    
    try:
        response = openai.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-mini"),
            messages=[{"role": m.role, "content": m.content} for m in request.messages],
            temperature=0.7,
        )
        
        return {"answer": response.choices[0].message.content}
    
    except Exception as e:
        logger.error(f"Error in /chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)