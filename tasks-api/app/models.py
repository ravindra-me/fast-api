# import al
from datetime import datetime;
from sqlalchemy import String, func, ForeignKey;
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database import Base

class Task(Base):
    __tablename__ = 'tasks'
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(100))
    done:Mapped[bool] = mapped_column(default=False)
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())
    user_id:Mapped[int | None]=mapped_column(ForeignKey('users.id'))
    # user: Mapped["User | None"] = relationship(back_populates="tasks")

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100))
    email:Mapped[str]= mapped_column(String(100))
    # tasks:Mapped[list["Task"]] = relationship(back_populates="User")