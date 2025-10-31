from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.team_member_schema import TeamMemberCreate, TeamMemberRead, TeamMemberUpdate
from app.services import team_member_service as TeamMemberService
from app.core.database import get_db

# Temporary: Get current user ID (same as teams)
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

router = APIRouter(prefix="/team-members", tags=["Team Members"])


@router.post("/teams/{team_id}/members", response_model=TeamMemberRead, status_code=status.HTTP_201_CREATED)
def add_member_to_team(
    team_id: int,
    member_data: TeamMemberCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Add a user to a team. Only team moderators can add members.
    """
    return TeamMemberService.add_member(db, team_id, current_user_id, member_data)


@router.get("/", response_model=list[TeamMemberRead])
def get_all_team_members(db: Session = Depends(get_db)):
    """
    Retrieve all team members from all teams.
    """
    return TeamMemberService.get_all_members(db)


@router.get("/{member_id}", response_model=TeamMemberRead)
def get_team_member_by_id(member_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single team member by ID.
    """
    return TeamMemberService.get_member_by_id(db, member_id)


@router.get("/teams/{team_id}/members", response_model=list[TeamMemberRead])  # ← ADICIONAR response_model
def get_members_of_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Retrieve all members of a specific team. Only team members can access this.
    """
    return TeamMemberService.get_team_members(db, team_id, current_user_id)


@router.put("/teams/{team_id}/members/{user_id}/role", response_model=TeamMemberRead)
def update_member_role(
    team_id: int,
    user_id: int,
    update_data: TeamMemberUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Update a member's role (moderator status). Only moderators can change roles.
    """
    return TeamMemberService.update_member_role(db, team_id, current_user_id, user_id, update_data)


@router.delete("/teams/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member_from_team(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Remove a user from a team. Only moderators can remove members.
    """
    TeamMemberService.remove_member(db, team_id, current_user_id, user_id)
    return None
