from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    is_moderator = Column(Boolean, default=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="teams")
