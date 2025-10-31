from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeamMemberBase(BaseModel):
    user_id: int
    team_id: int
    is_moderator: bool = False

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberUpdate(BaseModel):
    is_moderator: Optional[bool] = None

class TeamMemberRead(TeamMemberBase):
    id: int
    joined_at: datetime

    model_config = {
        "from_attributes": True
    }
