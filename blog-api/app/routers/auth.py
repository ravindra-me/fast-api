from fastapi import FastAPI, APIRouter, Depends, HTTPException 
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import hash_password, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.schemas import Token, UserOut, UserCreate

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/register", response_model=UserOut, status_code=201)
def create_user(payload:UserCreate, db:Session=Depends(get_db)):
    user = User(        
        name = payload.name,
        email = payload.email,
        password_hash = hash_password(payload.password)
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Email already registered')
    db.refresh(user)
    return user
      
@router.post("/login",response_model=Token)
def login(form:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.scalars(select(User).where(User.email == form.username)).first()
    if user is None or user.password_hash is None or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": create_access_token(user.id),"token_type": "bearer"}