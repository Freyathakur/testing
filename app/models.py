"""Data models for the Task Manager API"""

from pydantic import BaseModel, EmailStr
from typing import Optional


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
