from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class RequestStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In-Progress"
    RESOLVED = "Resolved"


class RegistrationStatus(Enum):
    CONFIRMED = "Confirmed"
    WAITLISTED = "Waitlisted"


class Event:
    def __init__(
        self,
        event_id: str,
        title: str,
        club: str,
        date: str,
        start_time: str,
        end_time: str,
        venue: str,
        max_seats: int,
    ):
        self.event_id = event_id
        self.title = title
        self.club = club
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.venue = venue
        self.max_seats = max_seats
        self.registrations: List[Registration] = []
        self.is_valid = True
        self.violations: List[str] = []
        self.created_at = datetime.now()

    def get_datetime_range(self) -> tuple[datetime, datetime]:
        start = datetime.strptime(f"{self.date} {self.start_time}", "%Y-%m-%d %I:%M %p")
        end = datetime.strptime(f"{self.date} {self.end_time}", "%Y-%m-%d %I:%M %p")
        return start, end

    def get_conflict_details(self, other: "Event") -> dict:
        """Get detailed information about any conflicts with another event."""
        conflicts = {
            "has_conflict": False,
            "venue_conflict": False,
            "time_conflict": False,
            "conflict_period": None,
        }

        # Check time conflict first
        self_start, self_end = self.get_datetime_range()
        other_start, other_end = other.get_datetime_range()

        if self_start <= other_end and self_end >= other_start:
            conflicts["time_conflict"] = True
            overlap_start = max(self_start, other_start)
            overlap_end = min(self_end, other_end)
            conflicts["conflict_period"] = {
                "start": overlap_start.strftime("%I:%M %p"),
                "end": overlap_end.strftime("%I:%M %p"),
                "date": self.date,
            }
            conflicts["has_conflict"] = True

        # Check venue conflict
        if self.venue == other.venue:
            conflicts["venue_conflict"] = True
            if conflicts["time_conflict"]:
                conflicts["has_conflict"] = True

        return conflicts

    def has_conflict_with(self, other: "Event") -> bool:
        conflict_details = self.get_conflict_details(other)
        return conflict_details["has_conflict"]

    def get_summary(self) -> Dict:
        confirmed = sum(
            1
            for reg in self.registrations
            if reg.status == RegistrationStatus.CONFIRMED
        )
        waitlisted = sum(
            1
            for reg in self.registrations
            if reg.status == RegistrationStatus.WAITLISTED
        )

        return {
            "event_id": self.event_id,
            "title": self.title,
            "date": self.date,
            "time": f"{self.start_time} - {self.end_time}",
            "venue": self.venue,
            "seats": {
                "max": self.max_seats,
                "confirmed": confirmed,
                "waitlisted": waitlisted,
            },
            "venue": self.venue,
            "violations": self.violations,
            "status": "Valid" if self.is_valid else "Invalid Schedule",
        }


class Student:
    def __init__(self, student_id: str, name: str = " "):
        self.student_id = student_id
        self.name = name or f"Test Subject {self.student_id}"
        self.registrations: List[Registration] = []
        self.service_requests: List[ServiceRequest] = []


class Registration:
    def __init__(self, student: Student, event: Event):
        self.student = student

        self.event = event
        self.status = RegistrationStatus.WAITLISTED


class ServiceRequest:
    def __init__(self, request_id: str, student: Student, category: str):
        self.request_id = request_id
        self.student = student
        self.category = category
        self.status = RequestStatus.OPEN
        self.created_at = datetime.now()
