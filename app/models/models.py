from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, Integer, String, Text
from datetime import datetime
from app.db.database import Base


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
