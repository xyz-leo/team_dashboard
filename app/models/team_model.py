from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Members association (TeamMember)
    members: Mapped[List["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    # Team tasks
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="team",
        cascade="all, delete-orphan"
    )

