from fastapi import APIRouter, UploadFile, File, Depends
import shutil
import os
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{datetime.now().timestamp()}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # пока просто заглушка анализа
    result = "Объект культурного наследия не обнаружен"

    return {
        "image_path": file_path,
        "result": result
    }
from database import get_connection

@router.post("/analyze")
async def analyze_image(user_id: int, file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{datetime.now().timestamp()}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = "Объект культурного наследия обнаружен"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analyses (user_id, image_path, result)
        VALUES (%s, %s, %s)
        """,
        (user_id, file_path, result)
    )

    conn.commit()

    return {"result": result}
@router.get("/history/{user_id}")
def get_history(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT image_path, result, created_at
        FROM analyses
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    return [
        {
            "image": r[0],
            "result": r[1],
            "date": str(r[2])
        }
        for r in rows
    ]