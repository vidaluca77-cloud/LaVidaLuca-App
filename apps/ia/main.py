from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional, Literal
import openai

load_dotenv()

app = FastAPI()

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def generate_guide(request: GuideRequest):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Vous êtes une IA d'assistance agricole, prudente et pratique.
        Question : {request.question}
        Activité : {request.activity_title or 'Non spécifié'}
        Niveau de sécurité : {request.safety_level}
        Durée : {request.duration_min} minutes
        Matériel requis : {', '.join(request.materials) if request.materials else 'Non spécifié'}
        """

        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-mini"),
            messages=[{"role": "system", "content": prompt}]
        )

        response = completion.choices[0].message.content

        return GuideResponse(
            title=request.activity_title or "Guide personnalisé",
            duration=f"{request.duration_min} min",
            materials=request.materials,
            rules=["Respecter les consignes", "Porter les équipements"],
            checklist=["Vérifier le matériel", "Suivre les étapes"],
            answer=response,
            question_echo=request.question
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-mini"),
            messages=[{"role": m.role, "content": m.content} for m in request.messages]
        )

        return {"answer": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))