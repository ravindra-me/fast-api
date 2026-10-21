from fastapi import FastAPI, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from app.models import Blog
from app.routers import users

app = FastAPI()


@app.get('/db-check')
def db_check(db:Session= Depends(get_db)):
    db.execute(text("select 1"))
    return {"database":"connected"}

@app.get("/test-blogs")
def test_blogs(db:Session=Depends(get_db)):
       blogs = db.scalars(select(Blog)).all()
       return [ {"title": blog.title,"author":blog.user.name} for blog in blogs]
   
   
app.include_router(users.router, prefix='/api/v1')


@app.get('/health')
def health():
    return {"status":"ok"}




