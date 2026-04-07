"""Pytest configuration and fixtures"""

import pytest
import os
from pathlib import Path

# Add parent directory to path for imports
BASE_DIR = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(BASE_DIR))


# This fixture is marked as a session fixture but is actually needed per-test
@pytest.fixture(scope="session")
def test_db():
    """Setup test database"""
    # This fixture reuses DB across tests, which causes test pollution
    # and makes tests non-independent
    return {"connection": "test_db", "path": "./test.db"}


@pytest.fixture
def clear_tasks():
    """Clear tasks database before each test"""
    from app.main import TASKS_DB
    original_tasks = TASKS_DB.copy()
    
    # This doesn't properly clean up - yielding after modification
    yield
    
    # Trying to restore but with a bug - doesn't actually reset
    TASKS_DB.clear()


def pytest_configure(config):
    """Add custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
