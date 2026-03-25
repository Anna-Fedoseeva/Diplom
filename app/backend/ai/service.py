import random
from sqlalchemy.orm import Session

from backend.database.models import CulturalObject, AnalysisResult


styles = [
    "Gothic",
    "Baroque",
    "Neoclassical",
    "Renaissance",
    "Modernism"
]


def analyze_object(db: Session, object_id: int):

    obj = db.query(CulturalObject).filter(
        CulturalObject.id == object_id
    ).first()

    if not obj:
        return None

    # mock анализ
    style = random.choice(styles)
    confidence = round(random.uniform(0.7, 0.95), 2)

    result = AnalysisResult(
        object_id=object_id,
        style=style,
        confidence=confidence
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result