from app.database import Base
from sqlalchemy import String, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class User(Base):
    __tablename__='users'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    email:Mapped[str] = mapped_column(String(100))
    created_at:Mapped[datetime]= mapped_column(server_default=func.now())
    blogs:Mapped[list["Blog"]] = relationship(back_populates="user")
    
    
class Blog(Base):
    __tablename__='blogs'
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String(200))
    content:Mapped[str]=mapped_column(Text)
    published:Mapped[bool]=mapped_column(default=False)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    created_at:Mapped[datetime]= mapped_column(server_default=func.now())
    user:Mapped[User | None]=relationship(back_populates='blogs')