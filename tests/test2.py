import os
import sys
from enum import Enum

from main import CampusEventManagementSystem
from models import RequestStatus

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# class RequestStatus(Enum):
#     OPEN = "Open"
#     IN_PROGRESS = "In-Progress"
#     RESOLVED = "Resolved"
def showcase():
    system = CampusEventManagementSystem()

    print("=== ADDING EVENTS ===")
    e1 = system.add_event(
        "E001",
        "Tech Talk",
        "Tech Club",
        "2025-09-20",
        "10:00 AM",
        "12:00 PM",
        "Auditorium",
        2,
    )
    e2 = system.add_event(
        "E002",
        "Workshop",
        "Coding Club",
        "2025-09-20",
        "11:00 AM",
        "01:00 PM",
        "Auditorium",
        3,
    )  # conflict: same venue & overlap
    e3 = system.add_event(
        "E003",
        "Dance Show",
        "Cultural Club",
        "2025-09-20",
        "02:00 PM",
        "04:00 PM",
        "Open Grounds",
        5,
    )  # no conflict

    print(system.get_event_summary("E001"))
    print(system.get_event_summary("E002"))  # should show conflict
    print(system.get_event_summary("E003"))

    print("\n=== ADDING STUDENTS ===")
    s1 = system.add_student("S001", "Alice")
    s2 = system.add_student("S002", "Bob")
    s3 = system.add_student("S003", "Charlie")

    print("Students added:", [s.student_id for s in system.students.values()])

    print("\n=== REGISTERING STUDENTS ===")
    r1 = system.register_for_event("S001", "E001")
    r2 = system.register_for_event("S002", "E001")
    r3 = system.register_for_event("S003", "E001")  # waitlisted (since max seats=2)

    print("Registration statuses for E001:")
    for reg in system.events["E001"].registrations:
        print(reg.student.student_id, reg.status.value)

    print("\n=== RAISING SERVICE REQUESTS ===")
    sr1 = system.raise_service_request("SR001", "S001", "Technical Support")
    sr2 = system.raise_service_request("SR002", "S002", "Food Issue")
    sr3 = system.raise_service_request("SR003", "S001", "Transport")

    print("Service Request Summary (initial):", system.get_service_request_summary())

    print("\n=== UPDATING SERVICE REQUEST STATUS ===")
    system.update_service_request_status("SR001", RequestStatus.IN_PROGRESS)
    system.update_service_request_status("SR002", RequestStatus.RESOLVED)

    print(
        "Service Request Summary (after updates):", system.get_service_request_summary()
    )

    print(system.display_events_summary(system.events))


if __name__ == "__main__":
    showcase()
