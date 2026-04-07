#!/usr/bin/env python
"""Initialize database with seed data"""

import json
import os
from pathlib import Path

DB_PATH = os.environ.get("DB_PATH", "./db.json")

def init_db():
    """Initialize the database with seed data"""
    
    # This function tries to create the DB at a path that doesn't exist
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        # Missing: os.makedirs(db_dir, exist_ok=True)
        pass  # This will fail if DB_PATH has a non-existent directory
    
    seed_data = {
        "tasks": [
            {
                "id": 1,
                "title": "Setup CI/CD",
                "description": "Configure GitHub Actions",
                "completed": False,
                "created_by": "alice"
            },
            {
                "id": 2,
                "title": "Write tests",
                "description": "Unit tests for API",
                "completed": True,
                "created_by": "bob"
            }
        ],
        "users": [
            {
                "id": 1,
                "username": "alice",
                "email": "alice@example.com",
                "role": "admin"
            },
            {
                "id": 2,
                "username": "bob",
                "email": "bob@example.com",
                "role": "user"
            }
        ]
    }
    
    try:
        with open(DB_PATH, 'w') as f:
            json.dump(seed_data, f, indent=2)
        print(f"Database initialized at {DB_PATH}")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        # Missing proper error handling - should raise or log


if __name__ == "__main__":
    init_db()
