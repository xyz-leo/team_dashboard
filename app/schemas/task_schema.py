from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    due_date: Optional[datetime] = None
    owner_id: int  # ← OBRIGATÓRIO!
    team_id: Optional[int] = None  # ← OPCIONAL


class TaskCreate(TaskBase):
    # Agora owner_id é obrigatório, team_id opcional
    pass


class TaskUpdate(BaseModel):
    """
    Schema used for updating a task.
    All fields are optional for partial updates.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    owner_id: Optional[int] = None  # Pode atualizar o dono
    team_id: Optional[int] = None   # Pode atualizar/remover o time

    model_config = {
        "from_attributes": True
    }


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
