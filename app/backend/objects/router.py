from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.objects.schemas import ObjectCreate, ObjectResponse
import backend.objects.service as service

router = APIRouter(prefix="/objects", tags=["objects"])


@router.post("/", response_model=ObjectResponse)
def create_object(obj: ObjectCreate, db: Session = Depends(get_db)):

    new_obj = service.create_object(db, obj, user_id=1)

    return new_obj


@router.get("/", response_model=list[ObjectResponse])
def get_objects(db: Session = Depends(get_db)):

    return service.get_objects(db)


@router.get("/{object_id}", response_model=ObjectResponse)
def get_object(object_id: int, db: Session = Depends(get_db)):

    obj = service.get_object(db, object_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")

    return obj


@router.delete("/{object_id}")
def delete_object(object_id: int, db: Session = Depends(get_db)):

    service.delete_object(db, object_id)

    return {"status": "deleted"}