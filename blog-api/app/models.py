from datetime import datetime

from sqlalchemy import ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    password_hash: Mapped[str | None] = mapped_column(String(255))
    blogs: Mapped[list["Blog"]] = relationship(back_populates="user")


class Blog(Base):
    __tablename__ = "blogs"
    __table_args__ = (Index("idx_blogs_user_published", "user_id", "published"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    published: Mapped[bool] = mapped_column(default=False, server_default="false")
    # views: Mapped[int] = mapped_column(default=0, server_default="0")
    view_count: Mapped[int] = mapped_column(default=0, server_default="0")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="blogs")

    @property
    def author_name(self) -> str:
        return self.user.name