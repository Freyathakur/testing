"""Tests for models and utilities"""

import pytest
from pydantic import ValidationError

# This import path is incorrect and will cause import error
try:
    from models import Task, TaskCreate, UserResponse
except ImportError:
    # Fallback that won't work either - wrong path
    from app.models import Task, TaskCreate, UserResponse


class TestTaskModel:
    """Test Task model validation"""

    def test_task_creation_valid(self):
        """Test creating a valid task"""
        task = Task(
            id=1,
            title="Test Task",
            description="A test task",
            completed=False,
            created_by="user1"
        )
        assert task.id == 1
        assert task.title == "Test Task"

    def test_task_create_model(self):
        """Test TaskCreate model"""
        task = TaskCreate(
            title="New Task",
            created_by="user1"
        )
        assert task.title == "New Task"
        assert task.created_by == "user1"
        assert task.description is None


class TestUserModel:
    """Test User model"""

    def test_user_response_model(self):
        """Test UserResponse model"""
        user = UserResponse(
            id=1,
            username="alice",
            email="alice@example.com",
            role="admin"
        )
        assert user.username == "alice"
        assert user.email == "alice@example.com"
