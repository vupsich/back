from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from app.auth import get_current_user
from . import models, schemas, utils
from .database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter(prefix="/api")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Сопоставление русских значений с ожидаемыми значениями в БД
    gender_mapping = {
        "Мужской": "male",
        "Женский": "female"
    }

    # Проверка соответствия полов
    if user.gender not in gender_mapping:
        raise HTTPException(status_code=400, detail="Invalid gender value. Allowed: Мужской, Женский.")

    # Преобразование значения gender перед сохранением
    user.gender = gender_mapping[user.gender]
    
    # Проверка совпадения паролей
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Хэширование пароля
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        gender=user.gender,  # Уже преобразованное значение
        birth_date=user.birth_date,
        city=user.city,
        language=user.language,
        hashed_password=hashed_password
    )
    # Сохранение в БД
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Логин пользователя через форму OAuth2PasswordRequestForm.
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()  # email вместо username
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(
    data={"sub": user.email}
)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected", response_model=schemas.UserResponse)
def protected_route(current_user: schemas.UserResponse = Depends(get_current_user)):
    """Пример защищённого маршрута."""
    return current_user