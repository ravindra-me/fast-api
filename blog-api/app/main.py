from fastapi import FastAPI, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from app.models import Blog
from app.routers import auth, users, blogs
from app.security import hash_password, verify_password

app = FastAPI()


@app.get("/test-hash")
def test_hash(password: str):
    h1 = hash_password(password)
    h2 = hash_password(password)
    return {
        "hash_1": h1,
        "hash_2": h2,
        "same_hash": h1 == h2,
        "verify_correct": verify_password(password, h1),
        "verify_wrong": verify_password("wrong", h1),
    }

@app.get('/db-check')
def db_check(db:Session= Depends(get_db)):
    db.execute(text("select 1"))
    return {"database":"connected"}

@app.get("/test-blogs")
def test_blogs(db:Session=Depends(get_db)):
       blogs = db.scalars(select(Blog)).all()
       return [ {"title": blog.title,"author":blog.user.name} for blog in blogs]
   
   
app.include_router(users.router, prefix='/api/v1')
app.include_router(blogs.router, prefix='/api/v1')
app.include_router(auth.router, prefix="/api/v1")


@app.get('/health')
def health():
    return {"status":"ok"}




