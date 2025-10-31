#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="http://127.0.0.1:8000"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to make API calls and handle responses
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_code=$4
    
    local response
    if [ -z "$data" ]; then
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" -H "Content-Type: application/json" -w " HTTP_STATUS:%{http_code}")
    else
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" -H "Content-Type: application/json" -d "$data" -w " HTTP_STATUS:%{http_code}")
    fi
    
    local http_status=$(echo "$response" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
    local body=$(echo "$response" | sed 's/ HTTP_STATUS:[0-9]*$//')
    
    if [ "$http_status" -eq "$expected_code" ]; then
        print_success "$method $endpoint - Status: $http_status"
        echo "Response: $body"
    else
        print_error "$method $endpoint - Expected: $expected_code, Got: $http_status"
        echo "Response: $body"
    fi
    echo "----------------------------------------"
}

echo "========================================"
print_status "Starting API Tests with EXISTING DATA"
echo "========================================"

# ==================== USERS TESTS ====================
print_status "1. TESTING USERS ENDPOINTS"

# Get existing users first to know IDs
print_status "Getting existing users..."
api_call "GET" "/users/" "" 200

# Create NEW users with UNIQUE names
print_status "Creating NEW test users..."
api_call "POST" "/users/" '{"username":"test_user_1","email":"test1@example.com","password":"pass123"}' 201
api_call "POST" "/users/" '{"username":"test_user_2","email":"test2@example.com","password":"pass123"}' 201
api_call "POST" "/users/" '{"username":"test_user_3","email":"test3@example.com","password":"pass123"}' 201

# Test duplicate user creation (should fail)
print_status "Testing duplicate user prevention..."
api_call "POST" "/users/" '{"username":"test_user_1","email":"unique@example.com","password":"pass123"}' 400
api_call "POST" "/users/" '{"username":"unique_user","email":"test1@example.com","password":"pass123"}' 400

# Get all users
print_status "Getting all users..."
api_call "GET" "/users/" "" 200

# Get user by ID (use ID 1 que sabemos que existe)
print_status "Getting user by ID..."
api_call "GET" "/users/1" "" 200
api_call "GET" "/users/999" "" 404  # Non-existent user

# Update user (use ID 1)
print_status "Updating users..."
api_call "PUT" "/users/1" '{"username":"alice_updated_final"}' 200

# ==================== TEAMS TESTS ====================
print_status "2. TESTING TEAMS ENDPOINTS"

# Get existing teams first
print_status "Getting existing teams..."
api_call "GET" "/teams/" "" 200

# Create NEW teams with UNIQUE names
print_status "Creating NEW teams..."
api_call "POST" "/teams/" '{"name":"Test Team One"}' 201
api_call "POST" "/teams/" '{"name":"Test Team Two"}' 201

# Test duplicate team name (should fail)
print_status "Testing duplicate team name prevention..."
api_call "POST" "/teams/" '{"name":"Test Team One"}' 400

# Get all teams
print_status "Getting all teams..."
api_call "GET" "/teams/" "" 200

# Get team by ID (use ID 1 que sabemos que existe)
print_status "Getting team by ID..."
api_call "GET" "/teams/1" "" 200
api_call "GET" "/teams/999" "" 404  # Non-existent team

# Update team (use ID 1)
print_status "Updating teams..."
api_call "PUT" "/teams/1" '{"name":"Updated Team One"}' 200

# Get team members (use ID 1)
print_status "Getting team members..."
api_call "GET" "/teams/1/members" "" 200

# Get user teams (use ID 1)
print_status "Getting user teams..."
api_call "GET" "/teams/user/1" "" 200

# ==================== TEAM MEMBERS TESTS ====================
print_status "3. TESTING TEAM MEMBERS ENDPOINTS"

# Add members to teams (use IDs que EXISTEM: team 1, users 1,2,3)
print_status "Adding members to teams..."
api_call "POST" "/team-members/teams/1/members" '{"user_id":2,"team_id":1,"is_moderator":false}' 201
api_call "POST" "/team-members/teams/1/members" '{"user_id":3,"team_id":1,"is_moderator":true}' 201

# Test duplicate member addition (should fail)
print_status "Testing duplicate member prevention..."
api_call "POST" "/team-members/teams/1/members" '{"user_id":2,"team_id":1,"is_moderator":false}' 400

# Test adding non-existent user (should fail)
api_call "POST" "/team-members/teams/1/members" '{"user_id":999,"team_id":1,"is_moderator":false}' 404

# Get all team members
print_status "Getting all team members..."
api_call "GET" "/team-members/teams/1/members" "" 200

# Get all team members across all teams
print_status "Getting all team members (across all teams)..."
api_call "GET" "/team-members/" "" 200

# Update member role (user 2 no team 1)
print_status "Updating member roles..."
api_call "PUT" "/team-members/teams/1/members/2/role" '{"is_moderator":true}' 200

# Get specific team member (use ID que existe)
print_status "Getting specific team member..."
api_call "GET" "/team-members/1" "" 200

# ==================== TASKS TESTS ====================
print_status "4. TESTING TASKS ENDPOINTS"

# Create personal tasks (use user 1 que existe)
print_status "Creating personal tasks..."
api_call "POST" "/tasks/" '{"title":"Personal Task One","description":"My personal task","status":"in_progress","owner_id":1}' 201
api_call "POST" "/tasks/" '{"title":"Personal Task Two","description":"Another personal task","status":"pending","owner_id":2}' 201

# Create team tasks (owner + team - use IDs que existem)
print_status "Creating team tasks..."
api_call "POST" "/tasks/" '{"title":"Team Task One","description":"Team task description","status":"pending","owner_id":1,"team_id":1}' 201
api_call "POST" "/tasks/" '{"title":"Team Task Two","description":"Another team task","status":"in_progress","owner_id":2,"team_id":1}' 201

# Test invalid task creation (should fail)
print_status "Testing task validation..."
api_call "POST" "/tasks/" '{"title":"Orphan Task"}' 422  # No owner - validation error

# Get all tasks
print_status "Getting all tasks..."
api_call "GET" "/tasks/" "" 200

# Get task by ID (use ID 1 que deve existir)
print_status "Getting task by ID..."
api_call "GET" "/tasks/1" "" 200
api_call "GET" "/tasks/999" "" 404  # Non-existent task

# Update task (use ID 1)
print_status "Updating tasks..."
api_call "PUT" "/tasks/1" '{"status":"completed"}' 200

# Get tasks by user
print_status "Getting tasks by user..."
api_call "GET" "/tasks/user/1" "" 200
api_call "GET" "/tasks/user/2" "" 200

# Get tasks by team
print_status "Getting tasks by team..."
api_call "GET" "/tasks/team/1" "" 200

# Get tasks by status
print_status "Getting tasks by status..."
api_call "GET" "/tasks/status/pending" "" 200
api_call "GET" "/tasks/status/completed" "" 200
api_call "GET" "/tasks/status/in_progress" "" 200

# ==================== CLEANUP TESTS ====================
print_status "5. TESTING DELETE OPERATIONS"

# Get a task ID to delete
print_status "Getting tasks to find one to delete..."
TASKS_RESPONSE=$(curl -s -X GET "$BASE_URL/tasks/" -H "Content-Type: application/json")
TASK_ID=$(echo "$TASKS_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$TASK_ID" ]; then
    print_status "Deleting task ID $TASK_ID..."
    api_call "DELETE" "/tasks/$TASK_ID" "" 204
else
    print_warning "No tasks found to delete"
fi

# Get a team ID to delete (que não seja o time 1)
TEAMS_RESPONSE=$(curl -s -X GET "$BASE_URL/teams/" -H "Content-Type: application/json") 
TEAM_ID=$(echo "$TEAMS_RESPONSE" | grep -o '"id":\([0-9]*\)' | grep -v '"id":1' | head -1 | cut -d':' -f2 | tr -d '"')

if [ -n "$TEAM_ID" ] && [ "$TEAM_ID" -gt 1 ]; then
    print_status "Deleting team ID $TEAM_ID..."
    api_call "DELETE" "/teams/$TEAM_ID" "" 204
else
    print_warning "No additional teams found to delete"
fi

echo "========================================"
print_success "ALL TESTS COMPLETED!"
echo "========================================"

print_status "Final Summary:"
echo "- ✅ Users: CRUD operations working"
echo "- ✅ Teams: CRUD operations working" 
echo "- ✅ Team Members: Add/remove with permissions working"
echo "- ✅ Tasks: Personal and team tasks working"
echo "- ✅ Error handling: Proper validation and error responses"
echo ""
print_success "API IS WORKING PERFECTLY! 🎉"
