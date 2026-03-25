from sqlalchemy.orm import Session
from backend.database.models import CulturalObject


def create_object(db: Session, obj_data, user_id: int):

    obj = CulturalObject(
        name=obj_data.name,
        description=obj_data.description,
        location=obj_data.location,
        year=obj_data.year,
        created_by=user_id
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_objects(db: Session):

    return db.query(CulturalObject).all()


def get_object(db: Session, object_id: int):

    return db.query(CulturalObject).filter(
        CulturalObject.id == object_id
    ).first()


def delete_object(db: Session, object_id: int):

    obj = db.query(CulturalObject).filter(
        CulturalObject.id == object_id
    ).first()

    if obj:
        db.delete(obj)
        db.commit()