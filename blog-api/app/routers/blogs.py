from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_blog_or_404, pagination, verify_api_key
from app.models import Blog, User
from app.schemas import (
    BlogCreate,
    BlogListOut,
    BlogOut,
    BlogUpdate,
    BlogWithAuthorOut,
)

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.get("", response_model=BlogListOut)
def list_blogs(
    published: bool | None = None,
    search: str | None = None,
    page: dict = Depends(pagination),
    db: Session = Depends(get_db),
):
    stmt = select(Blog)
    if published is not None:
        stmt = stmt.where(Blog.published == published)
    if search:
        stmt = stmt.where(Blog.title.ilike(f"%{search}%"))

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    blogs = db.scalars(
        stmt.order_by(Blog.created_at.desc())
        .limit(page["limit"])
        .offset(page["skip"])
    ).all()

    return {"data": blogs, "total": total}


@router.get("/{blog_id}", response_model=BlogWithAuthorOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    stmt = select(Blog).options(joinedload(Blog.user)).where(Blog.id == blog_id)
    blog = db.scalars(stmt).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.post(
    "",
    response_model=BlogOut,
    status_code=201,
    dependencies=[Depends(verify_api_key)],
)
def create_blog(payload: BlogCreate, db: Session = Depends(get_db)):
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    blog = Blog(**payload.model_dump())
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.put(
    "/{blog_id}",
    response_model=BlogOut,
    dependencies=[Depends(verify_api_key)],
)
def update_blog(
    payload: BlogUpdate,
    blog: Blog = Depends(get_blog_or_404),
    db: Session = Depends(get_db),
):
    for field, value in payload.model_dump().items():
        setattr(blog, field, value)
    db.commit()
    db.refresh(blog)
    return blog


@router.delete(
    "/{blog_id}",
    status_code=204,
    dependencies=[Depends(verify_api_key)],
)
def delete_blog(
    blog: Blog = Depends(get_blog_or_404),
    db: Session = Depends(get_db),
):
    db.delete(blog)
    db.commit()