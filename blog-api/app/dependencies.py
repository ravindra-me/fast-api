import secrets
from fastapi import Depends, HTTPException, Query, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import Blog
import jwt
from fastapi.security import OAuth2PasswordBearer
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

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


def get_current_user(token: str = Depends(oauth2_scheme), db:Session=Depends(get_db)):
        credentials_error = HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            user_id = int(payload["sub"])
        except (jwt.InvalidAlgorithmError, KeyError, ValueError):
            raise credentials_error
        user = db.get(User, user_id)
        if user is None:
            raise credentials_error
        return user