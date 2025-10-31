from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.team_model import Team
from app.models.team_member_model import TeamMember
from app.schemas.team_schema import TeamCreate, TeamUpdate


def create_team(db: Session, team_data: TeamCreate, creator_id: int) -> Team:
    """
    Create a new team and assign the creator as a moderator.
    
    Args:
        db: Database session
        team_data: Team creation data
        creator_id: ID of the user creating the team
        
    Returns:
        Team: Newly created team
        
    Raises:
        HTTPException: If team creation fails
    """
    try:
        from app.models.user_model import User
        creator = db.query(User).filter(User.id == creator_id).first()
        if not creator:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Creator user not found"
            )


        # Check if team name already exists
        existing_team = db.query(Team).filter(Team.name == team_data.name).first()
        if existing_team:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team name already exists"
            )
        
        # Create new team
        new_team = Team(name=team_data.name)
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        
        # Assign creator as moderator
        membership = TeamMember(
            user_id=creator_id,
            team_id=new_team.id,
            is_moderator=True
        )
        db.add(membership)
        db.commit()
        db.refresh(membership)
        db.refresh(new_team)  # Refresh to get relationships
        
        return new_team
        
    except HTTPException:
        # Re-raise HTTP exceptions
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating team: {str(e)}"
        )


def get_all_teams(db: Session) -> list[Team]:
    """
    Retrieve all teams from database.
    
    Args:
        db: Database session
        
    Returns:
        list[Team]: List of all teams
    """
    try:
        return db.query(Team).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving teams: {str(e)}"
        )


def get_team_by_id(db: Session, team_id: int) -> Team:
    """
    Retrieve a team by ID.
    
    Args:
        db: Database session
        team_id: ID of the team to retrieve
        
    Returns:
        Team: Requested team
        
    Raises:
        HTTPException: If team not found
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    return team


def update_team(db: Session, team_id: int, team_data: TeamUpdate) -> Team:
    """
    Update team information.
    
    Args:
        db: Database session
        team_id: ID of the team to update
        team_data: Data to update
        
    Returns:
        Team: Updated team
        
    Raises:
        HTTPException: If team not found or update fails
    """
    try:
        # Find team
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Update fields if provided
        update_data = team_data.model_dump(exclude_unset=True)
        
        if "name" in update_data and update_data["name"]:
            # Check if new name is taken by another team
            existing_team = db.query(Team).filter(
                Team.name == update_data["name"],
                Team.id != team_id
            ).first()
            if existing_team:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Team name already taken"
                )
            team.name = update_data["name"]
        
        # Commit changes
        db.commit()
        db.refresh(team)
        
        return team
        
    except HTTPException:
        # Re-raise HTTP exceptions
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating team: {str(e)}"
        )


def delete_team(db: Session, team_id: int) -> bool:
    """
    Delete a team by ID.
    
    Args:
        db: Database session
        team_id: ID of the team to delete
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: If team not found or deletion fails
    """
    try:
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Delete associated team members first (due to foreign key constraints)
        db.query(TeamMember).filter(TeamMember.team_id == team_id).delete()
        
        # Delete team tasks (if they exist)
        from app.models.task_model import Task
        db.query(Task).filter(Task.team_id == team_id).update({"team_id": None})
        
        # Delete the team
        db.delete(team)
        db.commit()
        
        return True
        
    except HTTPException:
        # Re-raise HTTP exceptions
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting team: {str(e)}"
        )


def get_team_members(db: Session, team_id: int) -> list[TeamMember]:
    """
    Retrieve all members of a specific team.
    """
    try:
        # Verify team exists
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Return all team members
        members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        return members
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving team members: {str(e)}"
        )


def get_user_teams(db: Session, user_id: int) -> list[Team]:
    """
    Retrieve all teams that a user is member of.
    
    Args:
        db: Database session
        user_id: ID of the user
        
    Returns:
        list[Team]: List of teams the user belongs to
    """
    try:
        return db.query(Team).join(TeamMember).filter(TeamMember.user_id == user_id).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user teams: {str(e)}"
        )
