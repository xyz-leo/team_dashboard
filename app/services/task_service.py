from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate) -> Task:
    """
    Create a new task in the database.
    """
    try:
        # Validate that owner exists
        from app.models.user_model import User
        from app.models.team_model import Team  # ← ADICIONAR ESTE IMPORT
        
        owner = db.query(User).filter(User.id == task_data.owner_id).first()
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task owner not found"
            )
        
        # If team_id provided, validate team exists
        if task_data.team_id is not None:
            team = db.query(Team).filter(Team.id == task_data.team_id).first()  # ← AGORA Team ESTÁ DEFINIDO
            if not team:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Team not found"
                )
        
        # Create new task
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            due_date=task_data.due_date,
            owner_id=task_data.owner_id,
            team_id=task_data.team_id
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        return new_task
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


def get_all_tasks(db: Session) -> list[Task]:
    """
    Retrieve all tasks from database.
    
    Args:
        db: Database session
        
    Returns:
        list[Task]: List of all tasks
    """
    try:
        return db.query(Task).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


def get_task_by_id(db: Session, task_id: int) -> Task:
    """
    Retrieve a task by ID.
    
    Args:
        db: Database session
        task_id: ID of the task to retrieve
        
    Returns:
        Task: Requested task
        
    Raises:
        HTTPException: If task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
    """
    Update task information.
    
    Args:
        db: Database session
        task_id: ID of the task to update
        task_data: Data to update
        
    Returns:
        Task: Updated task
        
    Raises:
        HTTPException: If task not found or update fails
    """
    try:
        # Find task
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Update fields if provided
        update_data = task_data.model_dump(exclude_unset=True)
        
        # Validate owner_id and team_id logic if being updated
        if 'owner_id' in update_data or 'team_id' in update_data:
            new_owner_id = update_data.get('owner_id', task.owner_id)
            new_team_id = update_data.get('team_id', task.team_id)
            
            if new_owner_id is None and new_team_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task must have either an owner or a team"
                )
            
            if new_owner_id is not None and new_team_id is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task cannot have both owner and team"
                )
        
        # Apply updates
        for field, value in update_data.items():
            if value is not None:  # Only update if value is provided
                setattr(task, field, value)
        
        # Commit changes
        db.commit()
        db.refresh(task)
        
        return task
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


def delete_task(db: Session, task_id: int) -> bool:
    """
    Delete a task by ID.
    
    Args:
        db: Database session
        task_id: ID of the task to delete
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: If task not found or deletion fails
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        db.delete(task)
        db.commit()
        
        return True
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )


def get_tasks_by_owner(db: Session, owner_id: int) -> list[Task]:
    """
    Retrieve all tasks owned by a specific user.
    
    Args:
        db: Database session
        owner_id: ID of the task owner
        
    Returns:
        list[Task]: List of tasks owned by the user
    """
    try:
        return db.query(Task).filter(Task.owner_id == owner_id).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user tasks: {str(e)}"
        )


def get_tasks_by_team(db: Session, team_id: int) -> list[Task]:
    """
    Retrieve all tasks assigned to a specific team.
    
    Args:
        db: Database session
        team_id: ID of the team
        
    Returns:
        list[Task]: List of tasks assigned to the team
    """
    try:
        return db.query(Task).filter(Task.team_id == team_id).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving team tasks: {str(e)}"
        )


def get_tasks_by_status(db: Session, status: str) -> list[Task]:
    """
    Retrieve all tasks with a specific status.
    
    Args:
        db: Database session
        status: Task status to filter by
        
    Returns:
        list[Task]: List of tasks with the specified status
    """
    try:
        return db.query(Task).filter(Task.status == status).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks by status: {str(e)}"
        )
