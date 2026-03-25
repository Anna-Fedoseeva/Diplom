from sqlalchemy import Column, Integer, String, ForeignKey, Float
from backend.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)


class CulturalObject(Base):
    __tablename__ = "cultural_objects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    description = Column(String)
    location = Column(String)
    year = Column(Integer)

    created_by = Column(Integer, ForeignKey("users.id"))

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    object_id = Column(Integer, ForeignKey("cultural_objects.id"))

    style = Column(String)
    confidence = Column(Float)