from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskRead
from app.services import task_service as TaskService
from app.core.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    Task must have either owner_id (personal task) or team_id (team task), but not both.
    """
    return TaskService.create_task(db, task_data)


@router.get("/", response_model=list[TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    """
    Retrieve all tasks.
    """
    return TaskService.get_all_tasks(db)


@router.get("/{task_id}", response_model=TaskRead)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by ID.
    """
    return TaskService.get_task_by_id(db, task_id)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task by ID.
    """
    return TaskService.update_task(db, task_id, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by ID.
    """
    TaskService.delete_task(db, task_id)
    return None


@router.get("/user/{user_id}", response_model=list[TaskRead])
def get_tasks_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all tasks owned by a specific user.
    """
    return TaskService.get_tasks_by_owner(db, user_id)


@router.get("/team/{team_id}", response_model=list[TaskRead])
def get_tasks_by_team(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all tasks assigned to a specific team.
    """
    return TaskService.get_tasks_by_team(db, team_id)


@router.get("/status/{status}", response_model=list[TaskRead])
def get_tasks_by_status(status: str, db: Session = Depends(get_db)):
    """
    Retrieve all tasks with a specific status.
    """
    return TaskService.get_tasks_by_status(db, status)
