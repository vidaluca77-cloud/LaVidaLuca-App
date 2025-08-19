from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="La Vida Luca IA (stub)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # à resserrer ensuite
    allow_methods=["*"],
    allow_headers=["*"],
)

class GuideReq(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/guide")
def guide(req: GuideReq):
    return {
        "title": "Conseil IA (stub)",
        "answer": "Le backend tourne. L’intégration OpenAI sera rebranchée ensuite.",
        "question_echo": req.question
    }
