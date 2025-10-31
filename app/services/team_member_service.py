from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.team_member_model import TeamMember
from app.models.team_model import Team
from app.models.user_model import User
from app.schemas.team_member_schema import TeamMemberCreate, TeamMemberUpdate


def add_member(db: Session, team_id: int, creator_id: int, new_member_data: TeamMemberCreate) -> TeamMember:
    """
    Add a new member to a team. Only moderators can add other users.
    
    Args:
        db: Database session
        team_id: ID of the team
        creator_id: ID of the user adding the member
        new_member_data: Data for the new member
        
    Returns:
        TeamMember: Newly created team member
        
    Raises:
        HTTPException: If operation fails
    """
    try:
        # Check if team exists
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )

        # Check if the creator is a moderator of the team
        creator_membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == team_id, TeamMember.user_id == creator_id)
            .first()
        )
        if not creator_membership or not creator_membership.is_moderator:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only moderators can add members"
            )

        # Check if the user to be added exists
        user = db.query(User).filter(User.id == new_member_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if the user is already part of the team
        existing_member = (
            db.query(TeamMember)
            .filter(
                TeamMember.team_id == team_id,
                TeamMember.user_id == new_member_data.user_id,
            )
            .first()
        )
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already in this team"
            )

        # Create the new team member
        team_member = TeamMember(
            user_id=new_member_data.user_id,
            team_id=team_id,
            is_moderator=new_member_data.is_moderator,
        )

        db.add(team_member)
        db.commit()
        db.refresh(team_member)
        
        return team_member
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding member to team: {str(e)}"
        )


def remove_member(db: Session, team_id: int, remover_id: int, user_id: int) -> bool:
    """
    Remove a member from a team. Only moderators can perform this action.
    
    Args:
        db: Database session
        team_id: ID of the team
        remover_id: ID of the user removing the member
        user_id: ID of the user to remove
        
    Returns:
        bool: True if removal was successful
        
    Raises:
        HTTPException: If operation fails
    """
    try:
        # Validate that the remover is a moderator
        remover_membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == team_id, TeamMember.user_id == remover_id)
            .first()
        )
        if not remover_membership or not remover_membership.is_moderator:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only moderators can remove members"
            )

        # Find the membership to remove
        membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
            .first()
        )
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found in this team"
            )

        db.delete(membership)
        db.commit()
        
        return True
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing member from team: {str(e)}"
        )


def update_member_role(db: Session, team_id: int, actor_id: int, user_id: int, update_data: TeamMemberUpdate) -> TeamMember:
    """
    Update moderator status for a team member. Only moderators can change roles.
    
    Args:
        db: Database session
        team_id: ID of the team
        actor_id: ID of the user performing the action
        user_id: ID of the user whose role is being updated
        update_data: Update data containing is_moderator flag
        
    Returns:
        TeamMember: Updated team member
        
    Raises:
        HTTPException: If operation fails
    """
    try:
        # Validate that the actor is a moderator
        actor_membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == team_id, TeamMember.user_id == actor_id)
            .first()
        )
        if not actor_membership or not actor_membership.is_moderator:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only moderators can change roles"
            )

        # Find target member
        member = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
            .first()
        )
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )

        # Update moderation status if provided
        if update_data.is_moderator is not None:
            member.is_moderator = update_data.is_moderator

        db.commit()
        db.refresh(member)
        
        return member
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating member role: {str(e)}"
        )


def get_team_members(db: Session, team_id: int, requester_id: int) -> list[TeamMember]:
    """
    Return all members of a given team. Only accessible to team members.
    """
    try:
        # Check if the requester is a member of the team
        requester_membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == team_id, TeamMember.user_id == requester_id)
            .first()
        )
        if not requester_membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: user is not a member of this team"
            )

        # Return all team members
        return db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving team members: {str(e)}"
        )


def get_member_by_id(db: Session, member_id: int) -> TeamMember:
    """
    Retrieve a team member by ID.
    
    Args:
        db: Database session
        member_id: ID of the team member
        
    Returns:
        TeamMember: Requested team member
        
    Raises:
        HTTPException: If team member not found
    """
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found"
        )
    return member


def get_all_members(db: Session) -> list[TeamMember]:
    """
    Retrieve all team members from all teams.
    
    Args:
        db: Database session
        
    Returns:
        list[TeamMember]: List of all team members
    """
    try:
        return db.query(TeamMember).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving all team members: {str(e)}"
        )
