import secrets
from fastapi import Depends, HTTPException, Query, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import Blog

api_key_header = APIKeyHeader(name="X-API-Key")
# pagination
def pagination(skip: int = 0, limit: int = Query(10, le=100)):
    return {"skip": skip, "limit": limit}

def verify_api_key(x_api_key: str = Security(api_key_header)):
    # compare_digest takes the same time for any input, so attackers can't guess the key char by char
    if not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
def get_blog_or_404(blog_id: int, db: Session = Depends(get_db)) -> Blog:
    blog = db.get(Blog, blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog