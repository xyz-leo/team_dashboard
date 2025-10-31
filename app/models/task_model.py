from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

from app.core.database import Base
from app.models.user_model import User


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # User relationship
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped[User] = relationship("User", back_populates="tasks")

    # Team relationship
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teams.id"), nullable=True)
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="tasks")
