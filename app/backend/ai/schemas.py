from pydantic import BaseModel


class AnalysisResponse(BaseModel):

    style: str
    confidence: float

    class Config:
        from_attributes = True