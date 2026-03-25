from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.auth.schemas import UserCreate, Token
import backend.auth.service as service
from backend.database.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        service.create_user(db, user.username, user.password)
        return {"status": "registered"}
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")


@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):

    auth_user = service.authenticate_user(db, user.username, user.password)

    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = service.create_access_token({"sub": auth_user.username})

    return {"access_token": token}