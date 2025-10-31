from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.team_schema import TeamCreate, TeamUpdate, TeamResponse
from app.schemas.team_member_schema import TeamMemberRead
from app.services import team_service as TeamService
from app.core.database import get_db

# Temporary: Get the first available user ID
def get_current_user_id(db: Session = Depends(get_db)):
    """
    Temporary function to get a valid user ID until authentication is implemented.
    Returns the ID of the first user in the database.
    """
    from app.models.user_model import User
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No users found. Please create a user first."
        )
    return user.id

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: TeamCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Create a new team.
    The creator will be automatically added as a moderator.
    """
    return TeamService.create_team(db, team_data, creator_id=current_user_id)


@router.get("/", response_model=list[TeamResponse])
def get_all_teams(db: Session = Depends(get_db)):
    """
    Retrieve all teams.
    """
    return TeamService.get_all_teams(db)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team_by_id(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific team by ID.
    """
    return TeamService.get_team_by_id(db, team_id)


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team_data: TeamUpdate, db: Session = Depends(get_db)):
    """
    Update a team's details.
    """
    return TeamService.update_team(db, team_id, team_data)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """
    Delete a team by ID.
    This will also remove all team members and unassign team tasks.
    """
    TeamService.delete_team(db, team_id)
    return None


@router.get("/{team_id}/members", response_model=list[TeamMemberRead])
def get_team_members(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all members of a specific team.
    """
    return TeamService.get_team_members(db, team_id)


@router.get("/user/{user_id}", response_model=list[TeamResponse])
def get_user_teams(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all teams that a user is member of.
    """
    return TeamService.get_user_teams(db, user_id)
