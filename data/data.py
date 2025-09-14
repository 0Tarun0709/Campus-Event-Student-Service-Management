# data.py

students = [
    "S101", "S102", "S103", "S104", "S105",
    "S201", "S202", "S203", "S204", "S205",
    "S301", "S302", "S303", "S304", "S305",
    "S401", "S402", "S403", "S404", "S405"
]

events = [
    {
        "event_id": "E101",
        "title": "AI Workshop",
        "club": "AI Club",
        "date": "2025-09-20",
        "start_time": "10:00 AM",
        "end_time": "12:00 PM",
        "venue": "Seminar Hall",
        "max_seats": 50
    },
    {
        "event_id": "E102",
        "title": "Guitar Jam",
        "club": "Music Club",
        "date": "2025-09-20",
        "start_time": "11:00 AM",
        "end_time": "12:30 PM",
        "venue": "Seminar Hall",  # ⛔ Conflict: same venue/time as E101
        "max_seats": 30
    },
    {
        "event_id": "E103",
        "title": "Coding Contest",
        "club": "Programming Club",
        "date": "2025-09-21",
        "start_time": "2:00 PM",
        "end_time": "5:00 PM",
        "venue": "Computer Lab",
        "max_seats": 40
    },
    {
        "event_id": "E104",
        "title": "Dance Competition",
        "club": "Dance Club",
        "date": "2025-09-22",
        "start_time": "3:00 PM",
        "end_time": "6:00 PM",
        "venue": "Auditorium",
        "max_seats": 25
    },
    {
        "event_id": "E105",
        "title": "Debate Championship",
        "club": "Debating Society",
        "date": "2025-09-23",
        "start_time": "1:00 PM",
        "end_time": "4:00 PM",
        "venue": "Conference Hall",
        "max_seats": 30
    },
    {
        "event_id": "E106",
        "title": "Robotics Expo",
        "club": "Robotics Club",
        "date": "2025-09-23",
        "start_time": "2:00 PM",
        "end_time": "4:00 PM",
        "venue": "Conference Hall",  # ⛔ Conflict with E105
        "max_seats": 27
    },
    {
        "event_id": "E107",
        "title": "Photography Contest",
        "club": "Photography Club",
        "date": "2025-09-25",
        "start_time": "2:00 PM",
        "end_time": "5:00 PM",
        "venue": "Art Gallery",
        "max_seats": 20
    },
    {
        "event_id": "E108",
        "title": "Startup Pitch",
        "club": "Entrepreneurship Cell",
        "date": "2025-09-26",
        "start_time": "10:00 AM",
        "end_time": "3:00 PM",
        "venue": "Conference Hall",
        "max_seats": 20
    },
    {
        "event_id": "E109",
        "title": "Hackathon",
        "club": "Tech Society",
        "date": "2025-09-27",
        "start_time": "9:00 AM",
        "end_time": "9:00 PM",
        "venue": "Innovation Hub",
        "max_seats":50
    },
    {
        "event_id": "E110",
        "title": "Cultural Night",
        "club": "Cultural Committee",
        "date": "2025-09-28",
        "start_time": "6:00 PM",
        "end_time": "11:00 PM",
        "venue": "Open Ground",
        "max_seats": 20
    },
    {
        "event_id": "E111",
        "title": "Drama Rehearsal",
        "club": "Drama Club",
        "date": "2025-09-28",
        "start_time": "7:00 PM",
        "end_time": "10:00 PM",
        "venue": "Open Ground",  # ⛔ Conflict with E110
        "max_seats": 50
    }
]

registrations = [
    ("S101", "E101"), ("S102", "E101"), ("S103", "E101"),
    ("S201", "E101"), ("S202", "E101"), ("S203", "E101"),
    ("S101", "E102"), ("S102", "E102"),
    ("S203", "E103"), ("S204", "E103"), ("S205", "E103"),
    ("S101", "E104"), ("S102", "E104"), ("S103", "E104"),
    ("S201", "E105"), ("S202", "E105"),
    ("S301", "E106"), ("S302", "E106"), ("S303", "E106"),
    ("S304", "E107"), ("S305", "E107"),
    ("S401", "E108"), ("S402", "E108"),
    ("S403", "E109"), ("S404", "E109"), ("S405", "E109"),
    ("S301", "E110"), ("S302", "E110"), ("S303", "E110"),
    ("S304", "E111"), ("S305", "E111")
]

service_requests = [
    ("R001", "S101", "Hostel Maintenance"),
    ("R002", "S102", "Library Access"),
    ("R003", "S103", "Counseling Appointment"),
    ("R004", "S201", "Hostel Maintenance"),
    ("R005", "S202", "Library Access"),
    ("R006", "S203", "Internet Issues"),
    ("R007", "S204", "Student ID Card"),
    ("R008", "S205", "Lab Access"),
    ("R009", "S301", "Sports Equipment"),
    ("R010", "S302", "Cafeteria Complaint"),
    ("R011", "S303", "Parking Access"),
    ("R012", "S304", "Scholarship Query"),
    ("R013", "S305", "Health Center Appointment"),
    ("R014", "S401", "Hostel Maintenance"),
    ("R015", "S402", "Library Access"),
    ("R016", "S403", "Lost & Found"),
    ("R017", "S404", "Exam Registration Issue"),
    ("R018", "S405", "Transport Facility")
]
