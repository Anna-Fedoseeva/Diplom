from sqlalchemy.orm import Session
from backend.database.models import User
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str):
    return pwd_context.verify(password, password_hash)


def create_user(db: Session, username: str, password: str):

    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        raise ValueError("User already exists")

    user = User(
        username=username,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, username: str, password: str):

    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token