from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import List, Optional, TYPE_CHECKING

# Import only for type checking to avoid circular imports
if TYPE_CHECKING:
    from .task_schema import TaskRead
    from .team_member_schema import TeamMemberRead

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class UserResponse(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }
