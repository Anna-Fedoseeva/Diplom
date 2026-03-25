from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.ai.schemas import AnalysisResponse
import backend.ai.service as service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/analyze/{object_id}", response_model=AnalysisResponse)
def analyze(object_id: int, db: Session = Depends(get_db)):

    result = service.analyze_object(db, object_id)

    if not result:
        raise HTTPException(status_code=404, detail="Object not found")

    return result