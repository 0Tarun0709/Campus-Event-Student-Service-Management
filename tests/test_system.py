import os
import sys

import pytest

from main import CampusEventManagementSystem
from models import Event, Registration, ServiceRequest, Student

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def system():
    """Create a fresh system instance for each test."""
    return CampusEventManagementSystem()


@pytest.fixture
def sample_student():
    """Create a sample student for testing."""
    return Student("S001", "John Doe")


@pytest.fixture
def sample_event():
    """Create a sample event for testing."""
    return Event(
        event_id="E001",
        title="AI Workshop",
        club="AI Club",
        date="2025-12-01",
        start_time="10:00 AM",
        end_time="12:00 PM",
        venue="Room 101",
        max_seats=50,
    )


class TestCampusEventManagementSystem:
    """Test suite for the Campus Event Management System."""

    def test_system_initialization(self, system):
        """Test that the system initializes correctly."""
        assert system is not None
        assert len(system.students) == 0
        assert len(system.events) == 0
        assert len(system.service_requests) == 0

    def test_add_student(self, system):
        """Test adding a student to the system."""
        result = system.add_student("S001", "John Doe")
        # Returns Student object, not string
        assert result is not None
        assert len(system.students) == 1
        assert result.student_id == "S001"

    def test_add_duplicate_student(self, system):
        """Test that adding a duplicate student returns existing student."""
        first_result = system.add_student("S001", "John Doe")
        second_result = system.add_student("S001", "Jane Doe")
        # Returns the existing student object
        assert first_result is second_result
        assert len(system.students) == 1

    def test_add_event(self, system):
        """Test adding an event to the system."""
        result = system.add_event(
            "E001",
            "AI Workshop",
            "AI Club",
            "2025-12-01",
            "10:00 AM",
            "12:00 PM",
            "Room 101",
            50,
        )
        # Returns Event object, not string
        assert result is not None
        assert len(system.events) == 1
        assert result.event_id == "E001"

    def test_event_conflict_detection(self, system):
        """Test that event conflicts are detected properly."""
        # Add first event
        system.add_event(
            "E001",
            "AI Workshop",
            "AI Club",
            "2025-12-01",
            "10:00 AM",
            "12:00 PM",
            "Room 101",
            50,
        )

        # Try to add conflicting event (same venue and time)
        result = system.add_event(
            "E002",
            "Python Workshop",
            "Coding Club",
            "2025-12-01",
            "11:00 AM",
            "1:00 PM",
            "Room 101",
            30,
        )
        # Event is created but marked as invalid due to conflict
        assert result is not None
        assert result.is_valid == False
        assert len(system.events) == 2

    def test_student_registration(self, system):
        """Test student registration for events."""
        # Add student and event first
        system.add_student("S001", "John Doe")
        system.add_event(
            "E001",
            "AI Workshop",
            "AI Club",
            "2025-12-01",
            "10:00 AM",
            "12:00 PM",
            "Room 101",
            50,
        )

        # Register student for event
        result = system.register_for_event("S001", "E001")
        assert result is not None
        # Check via event object
        event = system.events["E001"]
        assert len(event.registrations) == 1

    def test_registration_validation(self, system):
        """Test registration validation for non-existent student/event."""
        # Try to register non-existent student
        result = system.register_for_event("S999", "E001")
        assert result is None

        # Add student and try to register for non-existent event
        system.add_student("S001", "John Doe")
        result = system.register_for_event("S001", "E999")
        assert result is None

    @pytest.mark.slow
    def test_large_scale_operations(self, system):
        """Test system performance with larger datasets."""
        # Add many students
        for i in range(100):
            system.add_student(f"S{i:03d}", f"Student {i}")

        # Add many events
        for i in range(50):
            system.add_event(
                f"E{i:03d}",
                f"Event {i}",
                "Test Club",
                "2025-12-01",
                "10:00 AM",
                "12:00 PM",
                f"Room {i}",
                50,
            )

        assert len(system.students) == 100
        assert len(system.events) == 50

    def test_service_request_creation(self, system):
        """Test creating service requests."""
        system.add_student("S001", "John Doe")

        result = system.raise_service_request("R001", "S001", "Library Access")
        assert result is not None
        assert len(system.service_requests) == 1


class TestModels:
    """Test suite for individual model classes."""

    def test_student_creation(self):
        """Test Student model creation."""
        student = Student("S001", "John Doe")
        assert student.student_id == "S001"
        assert student.name == "John Doe"

    def test_event_creation(self):
        """Test Event model creation."""
        event = Event(
            "E001",
            "AI Workshop",
            "AI Club",
            "2025-12-01",
            "10:00 AM",
            "12:00 PM",
            "Room 101",
            50,
        )
        assert event.event_id == "E001"
        assert event.title == "AI Workshop"
        assert event.max_seats == 50
        assert len(event.registrations) == 0

    def test_registration_creation(self):
        """Test Registration model creation."""
        student = Student("S001", "John Doe")
        event = Event(
            "E001",
            "AI Workshop",
            "AI Club",
            "2025-12-01",
            "10:00 AM",
            "12:00 PM",
            "Room 101",
            50,
        )
        registration = Registration(student, event)
        assert registration.student.student_id == "S001"
        assert registration.event.event_id == "E001"
        assert registration.status is not None

    def test_service_request_creation(self):
        """Test ServiceRequest model creation."""
        student = Student("S001", "John Doe")
        request = ServiceRequest("R001", student, "Library Access")
        assert request.student.student_id == "S001"
        assert request.category == "Library Access"
        assert request.status is not None


if __name__ == "__main__":
    pytest.main([__file__])
