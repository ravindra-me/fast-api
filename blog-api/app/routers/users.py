from fastapi import FastAPI, APIRouter,Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut, BlogOut, UserReportOut


router = APIRouter(prefix='/users', tags=["users"])


@router.get('', response_model=list[UserOut], status_code=200)
def get_all_users(db:Session=Depends(get_db)):
    users = db.scalars(select(User)).all()
    return users

@router.post('', response_model= UserOut, status_code=201)
def create_user(payload:UserCreate,  db:Session = Depends(get_db)):
    user = User(**payload.model_dump())
    db.add(user)
    try:
        db.commit()  
    except IntegrityError:
        db.rollback()
        old = db.scalars(select(User).where(User.email==payload.email)).first()
        if old is not None:
           raise HTTPException(status_code=409, detail="Email already registered")
        raise HTTPException(status_code=400, detail="something went wrong")
    db.refresh(user)
    return user


# @router.get("/report", response_model=list[UserReportOut])
# def users_report(db: Session = Depends(get_db)):
#     users = db.scalars(select(User)).all()
#     return [{"name": u.name, "blog_count": len(u.blogs)} for u in users]

@router.get("/report", response_model=list[UserReportOut])
def users_report(db: Session = Depends(get_db)):
    stmt = select(User).options(selectinload(User.blogs))
    users = db.scalars(stmt).all()
    return [{"name": u.name, "blog_count": len(u.blogs)} for u in users]

@router.get('/{user_id}', response_model=UserOut, status_code=200)
def get_user(user_id:int, db:Session = Depends(get_db)):
    find_user = db.get(User, user_id)
    if find_user is None:
        raise HTTPException(status_code=404, detail="this user is not exist")
    
    return find_user


@router.get("/{user_id}/blogs", response_model=list[BlogOut], status_code=200)
def get_user_blogs(user_id:int, db:Session=Depends(get_db)):
    find_user = db.get(User, user_id)
    if find_user is None:
            raise HTTPException(status_code=404, detail="this user is not exist")
    return find_user.blogs
