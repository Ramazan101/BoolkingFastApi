from fastapi import APIRouter, Depends, HTTPException
from booking_app.database.db import SessionLocal
from booking_app.database.models import UserProfile, RefreshToken
from booking_app.database.schema import UserProfileInputSchema, UserRegisterSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from booking_app.config import (SECRET_KEY,ALGORITHM,
                                ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME)
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta=None):
    return create_refresh_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))

@auth_router.post('/register', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if email_db:
        raise HTTPException(status_code=400, detail='Email already registered')
    if user_db:
        raise HTTPException(status_code=400, detail='Username already registered')
    hashed_password = get_password_hash(user.password)
    user_data = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=hashed_password,
        age=user.age,
        phone_number=user.phone_number
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'You have been registered'}


@auth_router.post('/login', response_model=dict)
async def login(user: UserRegisterSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=404, detail='User not found')
    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})
    token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(token_db)
    db.commit()
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}

@auth_router.post('logout', response_model=dict)
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(UserProfile).filter(UserProfile.username == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=404, detail='Token not found')
    db.delete(stored_token)
    db.commit()
    return {'message': 'You have been logged out'}


@auth_router.post('/refresh')
async def login_refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=404, detail='Token not found')
    access_token = create_access_token({'sub': stored_token.username})

    return {'access_token': access_token,'token_type': 'Bearer'}



