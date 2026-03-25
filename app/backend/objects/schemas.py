from pydantic import BaseModel


class ObjectCreate(BaseModel):
    name: str
    description: str
    location: str
    year: int


class ObjectResponse(BaseModel):
    id: int
    name: str
    description: str
    location: str
    year: int

    class Config:
        from_attributes = True