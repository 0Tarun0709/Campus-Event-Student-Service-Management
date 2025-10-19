from main import CampusEventManagementSystem


def main():
    # Initialize the system
    system = CampusEventManagementSystem()

    # Add some students
    students = ["S01", "S02", "S03", "S04", "S05", "S06"]
    for student_id in students:
        system.add_student(student_id)

    # Add events
    events = [
        {
            "event_id": "E101",
            "title": "AI Workshop",
            "club": "AI Club",
            "date": "2025-09-20",
            "start_time": "10:00 AM",
            "end_time": "12:00 PM",
            "venue": "Seminar Hall",
            "max_seats": 50,
        },
        {
            "event_id": "E102",
            "title": "Guitar Jam",
            "club": "Music Club",
            "date": "2025-09-20",
            "start_time": "11:00 AM",
            "end_time": "12:30 PM",
            "venue": "Seminar Hall",
            "max_seats": 30,
        },
        {
            "event_id": "E103",
            "title": "Coding Contest",
            "club": "Programming Club",
            "date": "2025-09-21",
            "start_time": "2:00 PM",
            "end_time": "5:00 PM",
            "venue": "Computer Lab",
            "max_seats": 40,
        },
    ]

    # Add events to system
    for event in events:
        system.add_event(**event)

    # Register students for events
    registrations = [
        ("S01", "E101"),
        ("S02", "E101"),
        ("S03", "E101"),
        ("S04", "E102"),
        ("S05", "E103"),
        ("S06", "E103"),
    ]

    for student_id, event_id in registrations:
        system.register_for_event(student_id, event_id)

    # Raise some service requests
    service_requests = [
        ("R001", "S01", "Hostel Maintenance"),
        ("R002", "S02", "Library Access"),
        ("R003", "S03", "Counseling Appointment"),
    ]

    for request_id, student_id, category in service_requests:
        system.raise_service_request(request_id, student_id, category)

    # Print event summaries
    print("\n=== Event Summaries ===")
    for event_id in ["E101", "E102", "E103"]:
        summary = system.get_event_summary(event_id)
        print(f"\nEvent Summary for {summary['title']} ({summary['event_id']}):")
        print(
            f"Seats: {summary['seats']['max']} | "
            f"Registrations: {summary['seats']['confirmed']} Confirmed, "
            f"{summary['seats']['waitlisted']} Waitlisted"
        )
        print(f"Venue: {summary['venue']}")
        if summary["violations"]:
            print(f"Violations: {', '.join(summary['violations'])}")
        else:
            print("Violations: None")
        print(f"Status: {summary['status']}")

    # Print service request summary
    print("\n=== Service Request Summary ===")
    request_summary = system.get_service_request_summary()
    for status, count in request_summary.items():
        if count > 0:
            print(f"{status}: {count}")


if __name__ == "__main__":
    main()
