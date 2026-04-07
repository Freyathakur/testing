from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
import os
from typing import List, Optional
import sys  # Unused import - will trigger flake8
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Task Manager API", version="1.0.0")

# Models
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_by: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    created_by: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str


# Simulated database
TASKS_DB = [
    {"id": 1, "title": "Setup CI/CD", "description": "Configure GitHub Actions", "completed": False, "created_by": "alice"},
    {"id": 2, "title": "Write tests", "description": "Unit tests for API", "completed": True, "created_by": "bob"},
]

USERS_DB = [
    {"id": 1, "username": "alice", "email": "alice@example.com", "role": "admin"},
    {"id": 2, "username": "bob", "email": "bob@example.com", "role": "user"},
]

# This will fail in CI because DB_PATH env var is not set
DB_PATH = os.environ.get("DB_PATH", "./db.json")


@app.get("/", tags=["Health Check"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
async def get_tasks(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Get all tasks with pagination"""
    return TASKS_DB[skip : skip + limit]


@app.post("/tasks", response_model=Task, tags=["Tasks"])
async def create_task(task: TaskCreate):
    """Create a new task - this will have a test that expects wrong status code"""
    # Create new task
    new_id = max([t["id"] for t in TASKS_DB]) + 1 if TASKS_DB else 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "completed": False,
        "created_by": task.created_by,
    }
    TASKS_DB.append(new_task)
    return new_task


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task(task_id: int):
    """Get a specific task by ID"""
    for task in TASKS_DB:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: int, task_update: TaskCreate):
    """Update a task"""
    for i, task in enumerate(TASKS_DB):
        if task["id"] == task_id:
            TASKS_DB[i].update(task_update.dict(exclude_unset=True))
            return TASKS_DB[i]
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/users", response_model=List[UserResponse], tags=["Users"])
async def list_users():
    """List all users - this endpoint has an import issue in tests"""
    return USERS_DB


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: int):
    """Get a specific user by ID"""
    for user in USERS_DB:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/stats", tags=["Analytics"])
async def get_stats():
    """Get statistics - this line is too long and will trigger a style violation: ============================================"""
    completed = sum(1 for t in TASKS_DB if t["completed"])
    return {
        "total_tasks": len(TASKS_DB),
        "completed_tasks": completed,
        "pending_tasks": len(TASKS_DB) - completed,
        "users": len(USERS_DB),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
