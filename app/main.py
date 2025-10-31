from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db

# Import all route modules
from app.routers import (
    user_routes,
    team_routes,
    task_routes,
    team_member_routes,
)

init_db()  # Initialize the database connection

# Create the FastAPI application instance
app = FastAPI(
    title="Team Dashboard API",
    description="A prototype API for managing teams, tasks, and members. Built with FastAPI.",
    version="1.0.0",
)

# --- CORS Configuration ---
# Allows frontend clients (like a JS fetch on localhost) to access the API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Which domains can access the API
    allow_credentials=True,      # Allow cookies/auth headers
    allow_methods=["*"],         # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],         # Allow all headers
)

# --- Include all Routers ---
# Each router module handles a specific resource and its endpoints
app.include_router(user_routes.router)
app.include_router(team_routes.router)
app.include_router(task_routes.router)
app.include_router(team_member_routes.router)

# --- Root Route ---
@app.get("/")
def root():
    """
    Health check endpoint.
    Can be used to verify that the API is running.
    """
    return {"message": "Team Dashboard API is running successfully."}


# --- Application Events ---
# Optional startup and shutdown hooks

@app.on_event("startup")
def on_startup():
    """
    Code executed when the app starts.
    Good place to initialize connections or cache.
    """
    print("Application startup: resources initialized.")


@app.on_event("shutdown")
def on_shutdown():
    """
    Code executed when the app stops.
    Good place to close connections or cleanup.
    """
    print("Application shutdown: resources released.")

