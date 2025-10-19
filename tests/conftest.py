import os
import sys

import pytest

from main import CampusEventManagementSystem

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def system():
    """Create a fresh system instance for each test."""
    return CampusEventManagementSystem()


@pytest.fixture
def sample_student_data():
    """Sample student data for testing."""
    return {
        "student_id": "S001",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
    }


@pytest.fixture
def sample_event_data():
    """Sample event data for testing."""
    return {
        "event_id": "E001",
        "title": "Tech Workshop",
        "club": "Tech Club",
        "date": "2025-12-01",
        "start_time": "10:00 AM",
        "end_time": "12:00 PM",
        "venue": "Auditorium",
        "max_seats": 100,
    }


@pytest.fixture
def sample_service_request_data():
    """Sample service request data for testing."""
    return {
        "request_id": "R001",
        "student_id": "S001",
        "service_type": "Library",
        "description": "Book request",
        "priority": "Medium",
        "status": "Pending",
    }
