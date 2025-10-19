from datetime import datetime
from typing import Dict, List, Optional

from models import (
    Event,
    Registration,
    RegistrationStatus,
    RequestStatus,
    ServiceRequest,
    Student,
)


class CampusEventManagementSystem:
    """
    A comprehensive system for managing campus events, student registrations, and service requests.

    This class serves as the main controller for the entire campus event management system,
    handling event creation, student registration, conflict detection, and service requests.

    Attributes:
        events (Dict[str, Event]): Dictionary storing all events, keyed by event_id
        students (Dict[str, Student]): Dictionary storing all students, keyed by student_id
        service_requests (Dict[str, ServiceRequest]): Dictionary storing all service requests, keyed by request_id
    """

    def __init__(self):
        """
        Initialize the CampusEventManagementSystem with empty storage for events, students, and service requests.
        """
        self.events: Dict[str, Event] = {}
        self.students: Dict[str, Student] = {}
        self.service_requests: Dict[str, ServiceRequest] = {}

    def add_event(
        self,
        event_id: str,
        title: str,
        club: str,
        date: str,
        start_time: str,
        end_time: str,
        venue: str,
        max_seats: int,
    ) -> Event:
        """
        Add a new event to the system with automatic conflict detection.

        This function creates a new event and checks for any scheduling conflicts with existing events.
        If conflicts are found, the event's validity is determined based on registration order (first-come-first-valid).

        Args:
            event_id (str): Unique identifier for the event
            title (str): Name/title of the event
            club (str): Name of the organizing club
            date (str): Event date in YYYY-MM-DD format
            start_time (str): Event start time in HH:MM AM/PM format
            end_time (str): Event end time in HH:MM AM/PM format
            venue (str): Location where the event will be held
            max_seats (int): Maximum number of participants allowed

        Returns:
            Event: The newly created event object, with validity status and any conflict violations noted

        Note:
            - If the new event conflicts with an existing valid event, it will be marked as invalid
            - Conflicts can be either time-based, venue-based, or both
            - The first registered event in a conflict always remains valid
        """
        new_event = Event(
            event_id, title, club, date, start_time, end_time, venue, max_seats
        )

        ordered_events = sorted(self.events.values(), key=lambda x: x.created_at)

        for existing_event in ordered_events:
            conflict_details = existing_event.get_conflict_details(new_event)
            if conflict_details["has_conflict"]:
                if existing_event.is_valid:
                    new_event.is_valid = False
                    conflict_desc = []
                    if conflict_details["time_conflict"]:
                        period = conflict_details["conflict_period"]
                        if conflict_details["venue_conflict"]:
                            conflict_desc.append(
                                f"Time and venue conflict: Event at same venue ({new_event.venue}) "
                                f"on {period['date']} between {period['start']} and {period['end']}"
                            )
                        else:
                            conflict_desc.append(
                                f"Time conflict: Student cannot attend multiple events "
                                f"on {period['date']} between {period['start']} and {period['end']}"
                            )
                    new_event.violations.append(
                        f"Conflicts with {existing_event.title} ({existing_event.event_id}) which was registered first: "
                        + " - ".join(conflict_desc)
                    )
                    break

        self.events[event_id] = new_event
        return new_event

    def add_student(self, student_id: str, student_name: str = "") -> Student:
        """
        Add a new student to the system or retrieve existing student.

        Args:
            student_id (str): Unique identifier for the student
            student_name (str, optional): Name of the student. Defaults to empty string.

        Returns:
            Student: The newly created or existing student object

        Note:
            If a student with the given ID already exists, returns the existing student object
            instead of creating a new one.
        """
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, student_name)
        return self.students[student_id]

    def register_for_event(
        self, student_id: str, event_id: str
    ) -> Optional[Registration]:
        """
        Register a student for an event with automatic waitlist handling.

        This function handles the registration process including capacity checking
        and waitlist management. If the event is full, the registration will be
        automatically waitlisted.

        Args:
            student_id (str): ID of the student to register
            event_id (str): ID of the event to register for

        Returns:
            Optional[Registration]: Registration object if successful, None if student or event not found

        Note:
            - Returns existing registration if student is already registered
            - Automatically assigns CONFIRMED or WAITLISTED status based on event capacity
            - Updates both event and student registration lists
        """
        if event_id not in self.events or student_id not in self.students:
            return None

        event = self.events[event_id]
        student = self.students[student_id]

        for reg in event.registrations:
            if reg.student.student_id == student_id:
                return reg

        registration = Registration(student, event)

        # Check if seats are available
        confirmed_seats = sum(
            1
            for reg in event.registrations
            if reg.status == RegistrationStatus.CONFIRMED
        )

        if confirmed_seats < event.max_seats:
            registration.status = RegistrationStatus.CONFIRMED

        event.registrations.append(registration)
        student.registrations.append(registration)
        return registration

    def raise_service_request(
        self, request_id: str, student_id: str, category: str
    ) -> Optional[ServiceRequest]:
        """
        Create a new service request for a student.

        Args:
            request_id (str): Unique identifier for the service request
            student_id (str): ID of the student raising the request
            category (str): Category of the service request (e.g., "Academic", "Technical")

        Returns:
            Optional[ServiceRequest]: The created service request object, None if student not found

        Note:
            - Creates a new service request with initial status as OPEN
            - Links the request to both the system and the student's record
            - Automatically timestamps the request creation
        """
        if student_id not in self.students:
            return None

        student = self.students[student_id]
        request = ServiceRequest(request_id, student, category)
        self.service_requests[request_id] = request
        student.service_requests.append(request)
        return request

    # def get_event_status(self):

    def get_event_summary(self, event_id: str) -> Optional[Dict]:
        """
        Get a detailed summary of an event's status and registration information.

        Args:
            event_id (str): ID of the event to summarize

        Returns:
            Optional[Dict]: Dictionary containing event summary information including:
                - event_id: Event's unique identifier
                - title: Event name
                - date: Event date
                - time: Event timing
                - venue: Event location
                - seats: Dictionary containing max, confirmed, and waitlisted counts
                - violations: List of any scheduling violations
                - status: Event validity status
            Returns None if event not found

        Note:
            This is a comprehensive summary suitable for display and reporting purposes
        """
        if event_id not in self.events:
            return None
        return self.events[event_id].get_summary()

    def update_service_request_status(
        self, request_id: str, new_status: RequestStatus
    ) -> bool:
        """
        Update the status of an existing service request.

        Args:
            request_id (str): ID of the service request to update
            new_status (RequestStatus): New status to set (OPEN, IN_PROGRESS, or RESOLVED)

        Returns:
            bool: True if status was updated successfully, False if request not found

        Note:
            Uses the RequestStatus enum to ensure valid status values
        """
        if request_id in self.service_requests:
            self.service_requests[request_id].status = new_status
            return True
        return False

    def get_service_request_summary(self) -> Dict[str, int]:
        """
        Generate a summary of all service requests grouped by their status.

        Returns:
            Dict[str, int]: Dictionary with status values as keys and count of requests as values
                Example: {
                    "Open": 5,
                    "In-Progress": 3,
                    "Resolved": 10
                }

        Note:
            Initializes counters for all possible status values, even if count is 0
        """
        summary = {status.value: 0 for status in RequestStatus}
        for request in self.service_requests.values():
            summary[request.status.value] += 1
        return summary

    def display_events_summary(self, events):
        """
        Display a comprehensive summary of all events including conflicts and validity status.

        Args:
            events (Dict[str, Event]): Dictionary of events to analyze and display

        Displays:
            - Total number of events
            - Count of valid and invalid events
            - Number of events with conflicts
            - Total number of conflict pairs
            - Detailed conflict information (venue and time conflicts)
            - Events grouped by venue

        Note:
            This function prints the information directly rather than returning it
        """
        print("\nEVENTS SUMMARY")
        print("=" * 50)

        total_events = len(events)
        # valid_events = sum(1 for event in events[event] if event.is_valid)
        valid_events = 0
        # events=system.events
        for event in events:

            if events[event].is_valid:
                valid_events = valid_events + 1

        print(valid_events)
        invalid_events = total_events - valid_events

        events_with_conflicts = set()
        conflict_pairs = []

        for i, event1 in enumerate(events):
            for event2 in events:
                if events[event1].has_conflict_with(events[event2]):

                    events_with_conflicts.add(events[event1])
                    events_with_conflicts.add(events[event2])
                    conflict_pairs.append((events[event1], events[event2]))

        print(f"\nTotal Events: {total_events}")
        print(f"Valid Events: {valid_events}")
        print(f"Invalid Events: {invalid_events}")
        print(f"Events with Conflicts: {len(events_with_conflicts)}")
        print(f"Total Conflict Pairs: {len(conflict_pairs)}")

        # if conflict_pairs:
        #     print("\nConflict Details:")
        #     for events[event1], events[event2] in conflict_pairs:
        #         conflict_details = events[event1].get_conflict_details(events[event2])
        #         print(f"\n{events[event1].title} <-> {events[event2].title}")
        #         if conflict_details["venue_conflict"]:
        #             print(f"- Venue Conflict: {events[event1].venue}")
        #         if conflict_details["time_conflict"]:
        #             period = conflict_details["conflict_period"]
        #             print(f"- Time Conflict: {period['date']} {period['start']} - {period['end']}")

        # # Show events by venue
        # print("\nEvents by Venue:")
        # venues = {}
        # for event in events:
        #     if events[event].venue not in venues:
        #         venues[events[event].venue] = []
        #     venues[events[event].venue].append(events[event])

        # for venue, venue_events in venues.items():
        #     print(f"\n{venue}:")
        #     for event in venue_events:
        #         print(f"- {event.title} ({event.date} {event.start_time} - {event.end_time})")
