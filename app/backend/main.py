from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends
from backend.auth.dependencies import get_current_user
from backend.ai.mock import MockAIService
from backend.auth.router import router as auth_router
from backend.objects.router import router as objects_router
from backend.ai.router import router as ai_router

from backend.database.db import engine
from backend.database.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(objects_router)
app.include_router(ai_router)

ai_service = MockAIService()


class AnalyzeRequest(BaseModel):
    defect: str
    zone: str

@app.post("/analyze")
def analyze(req: AnalyzeRequest, user: str = Depends(get_current_user)):
    result = ai_service.analyze(req.defect, req.zone)

    return {
        "user": user,
        "result": result
    }