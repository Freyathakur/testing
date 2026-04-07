"""Unit tests for Task Manager API"""

import pytest
from fastapi.testclient import TestClient
import time
from datetime import datetime

# This import path is intentionally wrong - should be from app.main
from app.main import app, TASKS_DB, USERS_DB

client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_check_status(self):
        """Test that health check returns healthy status"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestTasks:
    """Test Task endpoints"""

    def test_get_tasks_empty(self):
        """Test getting tasks when list exists"""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_tasks_with_pagination(self):
        """Test pagination parameters"""
        response = client.get("/tasks?skip=0&limit=5")
        assert response.status_code == 200
        assert len(response.json()) <= 5

    def test_create_task_returns_wrong_status(self):
        """Create task endpoint should return 201, but test expects 200 - will fail"""
        task_data = {
            "title": "New Task",
            "description": "Test task",
            "created_by": "alice"
        }
        response = client.post("/tasks", json=task_data)
        # Expected 201 Created but endpoint returns 200 OK
        assert response.status_code == 200  # This will fail in a real scenario

    def test_get_task_by_id(self):
        """Test retrieving a specific task"""
        response = client.get("/tasks/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Setup CI/CD"

    def test_get_nonexistent_task(self):
        """Test that nonexistent task returns 404"""
        response = client.get("/tasks/99999")
        assert response.status_code == 404

    def test_update_task(self):
        """Test updating a task"""
        update_data = {
            "title": "Updated Task",
            "description": "Updated description",
            "created_by": "alice"
        }
        response = client.put("/tasks/1", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"


class TestUsers:
    """Test User endpoints"""

    def test_list_users(self):
        """Test listing users - import issue will cause this to fail"""
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) > 0
        assert users[0]["username"] == "alice"

    def test_get_user_by_id(self):
        """Test getting a specific user"""
        response = client.get("/users/1")
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == 1
        assert user["username"] == "alice"

    def test_get_nonexistent_user(self):
        """Test getting nonexistent user"""
        response = client.get("/users/9999")
        assert response.status_code == 404


class TestStats:
    """Test Statistics endpoint"""

    def test_get_stats(self):
        """Test getting stats - this test has a time-dependent assertion that could be flaky"""
        response = client.get("/stats")
        assert response.status_code == 200
        stats = response.json()
        assert "total_tasks" in stats
        assert "completed_tasks" in stats
        assert "pending_tasks" in stats
        assert stats["total_tasks"] >= 0


class TestFlaky:
    """Flaky test that depends on time"""

    def test_timestamp_is_recent(self):
        """This test is flaky if there's a CI delay or time skew"""
        response = client.get("/")
        data = response.json()
        timestamp_str = data["timestamp"]
        
        # Parse ISO format timestamp
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        
        # This will fail if the CI runner has a time sync issue or is slow
        # Allowing 5 second window, but this can flake
        time_diff = (now - timestamp).total_seconds()
        assert time_diff < 5, f"Timestamp too old: {time_diff} seconds"
