# Team Dashboard API

A comprehensive REST API for team management and task tracking built with FastAPI and PostgreSQL.

## Overview

This API provides a complete backend solution for managing teams, users, tasks, and team memberships. It features a clean architecture with proper separation of concerns, validation, and error handling.

## Features

- **User Management**: Complete CRUD operations for users with secure password hashing
- **Team Management**: Create and manage teams with automatic moderator assignment
- **Team Members**: Add/remove team members with role-based permissions
- **Task Management**: Personal and team tasks with flexible ownership
- **RESTful API**: Fully compliant REST endpoints with proper HTTP status codes
- **Data Validation**: Comprehensive input validation using Pydantic schemas
- **Error Handling**: Detailed error responses with appropriate status codes
- **Database Relationships**: Properly modeled relationships between all entities

## Technology Stack

- **Backend**: FastAPI, Python 3.13
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Password hashing with Argon2
- **Validation**: Pydantic v2 for data schemas and validation

## Project Structure

```
app/
├── core/
│ ├── config.py # Application configuration
│ └── database.py # Database connection and session management
├── models/ # SQLAlchemy database models
│ ├── user_model.py
│ ├── team_model.py
│ ├── team_member_model.py
│ └── task_model.py
├── schemas/ # Pydantic schemas for request/response validation
│ ├── user_schema.py
│ ├── team_schema.py
│ ├── team_member_schema.py
│ └── task_schema.py
├── services/ # Business logic layer
│ ├── user_service.py
│ ├── team_service.py
│ ├── team_member_service.py
│ └── task_service.py
├── routers/ # FastAPI route handlers
│ ├── user_routes.py
│ ├── team_routes.py
│ ├── team_member_routes.py
│ └── task_routes.py
├── utils/
│ ├── auth.py # Authentication utilities
│ └── testing_api.sh # Comprehensive API test script
├── main.py # FastAPI application entry point

```


## Data Models

### User
- Basic user information with secure password storage
- Relationships: tasks (owned), team_members (team participations)

### Team
- Team information and metadata
- Relationships: members, tasks (team tasks)

### TeamMember
- Junction table between users and teams
- Role-based permissions (member/moderator)
- Automatic timestamp for join date

### Task
- Flexible task ownership system
- Can belong to user only, or user + team
- Status tracking and due dates
- Automatic created/updated timestamps

## API Endpoints

### Users
- `POST /users/` - Create new user
- `GET /users/` - List all users
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Teams
- `POST /teams/` - Create new team (creator becomes moderator)
- `GET /teams/` - List all teams
- `GET /teams/{id}` - Get team by ID
- `PUT /teams/{id}` - Update team
- `DELETE /teams/{id}` - Delete team
- `GET /teams/{id}/members` - Get team members
- `GET /teams/user/{user_id}` - Get user's teams

### Team Members
- `POST /team-members/teams/{team_id}/members` - Add member to team
- `GET /team-members/teams/{team_id}/members` - Get team members
- `GET /team-members/` - Get all team memberships
- `GET /team-members/{id}` - Get specific team membership
- `PUT /team-members/teams/{team_id}/members/{user_id}/role` - Update member role
- `DELETE /team-members/teams/{team_id}/members/{user_id}` - Remove member from team

### Tasks
- `POST /tasks/` - Create new task
- `GET /tasks/` - List all tasks
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `GET /tasks/user/{user_id}` - Get user's tasks
- `GET /tasks/team/{team_id}` - Get team's tasks
- `GET /tasks/status/{status}` - Get tasks by status

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd team_dashboard
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt

```

4. Set up PostgreSQL database and update connection string in app/core/config.py

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## Key Design Decisions

    Layered Architecture: Clear separation between routes, services, and models

    Schema Validation: Pydantic schemas for all request/response data

    Business Logic in Services: Core logic separated from HTTP concerns

    Flexible Task Ownership: Tasks always have owners, optionally have teams

    Role-Based Permissions: Moderators can manage team members

    Comprehensive Error Handling: Meaningful error messages with proper HTTP codes


## Development

The codebase follows Python best practices with:

    Type hints throughout

    Comprehensive docstrings

    Consistent code style

    Modular and testable design


## License

This project is licensed under the MIT License.
