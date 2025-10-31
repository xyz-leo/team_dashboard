from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .task_schema import TaskRead
    from .team_member_schema import TeamMemberRead

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class TeamResponse(TeamBase):
    id: int

    model_config = {
        "from_attributes": True
    }
