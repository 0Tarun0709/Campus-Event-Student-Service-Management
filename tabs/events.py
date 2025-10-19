from datetime import datetime

import pandas as pd
import streamlit as st

from models import RegistrationStatus, RequestStatus

# Constants
TIME_FORMAT = "%I:%M %p"
DATE_FORMAT = "%Y-%m-%d"
EVENT_ADDED_MSG = "Event added successfully!"


def _format_conflict_message(other_event_title, conflict_details, venue):
    """Format a conflict description message."""
    conflict_desc = []
    if conflict_details["venue_conflict"]:
        conflict_desc.append(f"Venue conflict at {venue}")
    if conflict_details["time_conflict"]:
        period = conflict_details["conflict_period"]
        conflict_desc.append(
            f"Time overlap on {period['date']} between {period['start']} and {period['end']}"
        )
    return f"Conflicts with {other_event_title}: " + " AND ".join(conflict_desc)


def _check_event_conflicts(event_id, title, club, date, start_time, end_time, venue):
    """
    Check for scheduling conflicts with existing events.

    Args:
        event_id: ID of the event to check
        title: Event title
        club: Organizing club
        date: Event date
        start_time: Event start time
        end_time: Event end time
        venue: Event venue

    Returns:
        List of conflict descriptions
    """

    class TempEvent:
        def __init__(self, event_id, title, club, date, start_time, end_time, venue):
            self.event_id = event_id
            self.title = title
            self.club = club
            self.date = date.strftime(DATE_FORMAT)
            self.start_time = start_time.strftime(TIME_FORMAT)
            self.end_time = end_time.strftime(TIME_FORMAT)
            self.venue = venue

        def get_conflict_details(self, other_event):
            if hasattr(st.session_state.system, "get_event_conflict"):
                return st.session_state.system.get_event_conflict(self, other_event)

            # Minimal time and venue conflict check
            conflict = {
                "has_conflict": False,
                "venue_conflict": False,
                "time_conflict": False,
                "conflict_period": {},
            }

            if self.venue != other_event.venue or self.date != other_event.date:
                return conflict

            conflict["venue_conflict"] = True
            start1 = datetime.strptime(self.start_time, TIME_FORMAT)
            end1 = datetime.strptime(self.end_time, TIME_FORMAT)
            start2 = datetime.strptime(other_event.start_time, TIME_FORMAT)
            end2 = datetime.strptime(other_event.end_time, TIME_FORMAT)
            overlap = max(start1, start2) < min(end1, end2)

            if overlap:
                conflict["time_conflict"] = True
                conflict["has_conflict"] = True
                conflict["conflict_period"] = {
                    "date": self.date,
                    "start": max(start1, start2).strftime(TIME_FORMAT),
                    "end": min(end1, end2).strftime(TIME_FORMAT),
                }

            conflict["has_conflict"] = (
                conflict["venue_conflict"] or conflict["time_conflict"]
            )
            return conflict

    temp_event = TempEvent(event_id, title, club, date, start_time, end_time, venue)
    conflicts_list = []

    for other_event in st.session_state.system.events.values():
        if other_event.event_id == event_id:
            continue

        conflict_details = temp_event.get_conflict_details(other_event)
        if conflict_details["has_conflict"]:
            conflicts_list.append(
                _format_conflict_message(other_event.title, conflict_details, venue)
            )

    return conflicts_list


def _add_event_to_system(
    event_id, title, club, date, start_time, end_time, venue, max_seats
):
    """Add an event to the system."""
    st.session_state.system.add_event(
        event_id=event_id,
        title=title,
        club=club,
        date=date.strftime(DATE_FORMAT),
        start_time=start_time.strftime(TIME_FORMAT),
        end_time=end_time.strftime(TIME_FORMAT),
        venue=venue,
        max_seats=max_seats,
    )


def _render_add_event_form():
    """Render the form for adding a new event."""
    with st.expander("Add New Event"):
        col1, col2 = st.columns(2)
        with col1:
            event_id = st.text_input("Event ID")
            title = st.text_input("Event Title")
            club = st.text_input("Organizing Club")
            event_venue = st.text_input("Venue")
        with col2:
            date = st.date_input("Date")
            start_time = st.time_input("Start Time")
            end_time = st.time_input("End Time")
            max_seats = st.number_input("Maximum Seats", min_value=1, value=50)

        # Initialize session state flags
        if "conflict_warning" not in st.session_state:
            st.session_state.conflict_warning = False
        if "add_anyway" not in st.session_state:
            st.session_state.add_anyway = False

        _handle_add_event_button(
            event_id, title, club, date, start_time, end_time, event_venue, max_seats
        )
        _handle_conflict_warning(
            event_id, title, club, date, start_time, end_time, event_venue, max_seats
        )


def _handle_add_event_button(
    event_id, title, club, date, start_time, end_time, venue, max_seats
):
    """Handle the Add Event button click."""
    if st.button("Add Event") or st.session_state.add_anyway:
        if st.session_state.add_anyway:
            st.session_state.conflict_warning = False
            st.session_state.add_anyway = False
            _add_event_to_system(
                event_id, title, club, date, start_time, end_time, venue, max_seats
            )
            st.success(EVENT_ADDED_MSG)
        else:
            if all([event_id, title, club, venue]):
                conflicts_found = _check_event_conflicts(
                    event_id, title, club, date, start_time, end_time, venue
                )
                if conflicts_found and not st.session_state.add_anyway:
                    st.session_state.conflict_warning = conflicts_found
                else:
                    st.session_state.conflict_warning = False
                    st.session_state.add_anyway = False
                    _add_event_to_system(
                        event_id,
                        title,
                        club,
                        date,
                        start_time,
                        end_time,
                        venue,
                        max_seats,
                    )
                    st.success(EVENT_ADDED_MSG)
            else:
                st.error(
                    "Please fill in all required fields (Event ID, Title, Club, Venue)."
                )


def _handle_conflict_warning(
    event_id, title, club, date, start_time, end_time, venue, max_seats
):
    """Display and handle conflict warning popup."""
    if st.session_state.conflict_warning:
        st.warning("Detected scheduling conflicts with this event:")
        for conflict_text in st.session_state.conflict_warning:
            st.write(f"- {conflict_text}")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Change Event"):
                st.session_state.conflict_warning = False
        with col_b:
            if st.button("Add Anyway"):
                st.session_state.add_anyway = True
                _add_event_to_system(
                    event_id, title, club, date, start_time, end_time, venue, max_seats
                )
                st.success(EVENT_ADDED_MSG)


def _get_event_conflicts(event):
    """Get all conflicts for a specific event."""
    conflicts = []
    for other_event in st.session_state.system.events.values():
        if other_event.event_id != event.event_id:
            conflict_details = event.get_conflict_details(other_event)
            if conflict_details["has_conflict"]:
                conflict_desc = []
                if conflict_details["venue_conflict"]:
                    conflict_desc.append(f"Venue conflict at {event.venue}")
                if conflict_details["time_conflict"]:
                    period = conflict_details["conflict_period"]
                    conflict_desc.append(
                        f"Time overlap on {period['date']} between {period['start']} and {period['end']}"
                    )
                conflicts.append(
                    f"Conflicts with {other_event.title}: "
                    + " AND ".join(conflict_desc)
                )
    return conflicts


def _render_events_list():
    """Render the list of current events."""
    st.subheader("Current Events")
    if not st.session_state.system.events:
        st.info("No events available.")
        return

    event_data = []
    for event in st.session_state.system.events.values():
        summary = event.get_summary()
        conflicts = _get_event_conflicts(event)

        event_data.append(
            {
                "Event ID": event.event_id,
                "Title": event.title,
                "Date": event.date,
                "Time": f"{event.start_time} - {event.end_time}",
                "Venue": event.venue,
                "Available Seats": event.max_seats - summary["seats"]["confirmed"],
                "Status": summary["status"],
                "Conflicts": (
                    "\\n".join(conflicts)
                    if summary["status"] == "Invalid Schedule"
                    else "No conflicts"
                ),
            }
        )

    df = pd.DataFrame(event_data)
    st.dataframe(df)


def _render_event_details():
    """Render detailed view of a selected event."""
    st.subheader("Event Details & Registrations")
    selected_event = st.selectbox(
        "Select Event to View Details",
        options=list(st.session_state.system.events.keys()),
        key="event_details",
    )

    if not selected_event:
        return

    event = st.session_state.system.events[selected_event]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Seats", event.max_seats)
    with col2:
        confirmed = sum(
            1
            for reg in event.registrations
            if reg.status == RegistrationStatus.CONFIRMED
        )
        st.metric("Confirmed Registrations", confirmed)
    with col3:
        waitlisted = sum(
            1
            for reg in event.registrations
            if reg.status == RegistrationStatus.WAITLISTED
        )
        st.metric("Waitlisted", waitlisted)

    st.markdown("##### 👥 Registered Students")
    if event.registrations:
        registration_data = [
            {
                "Student ID": reg.student.student_id,
                "Student Name": reg.student.name,
                "Registration Status": reg.status.value,
                "Other Registrations": len(reg.student.registrations) - 1,
                "Service Requests": len(reg.student.service_requests),
            }
            for reg in event.registrations
        ]
        st.dataframe(pd.DataFrame(registration_data))
    else:
        st.info("No students registered for this event")


def _render_registration_form():
    """Render the student registration form."""
    st.subheader("Register for Event")
    col1, col2 = st.columns(2)

    with col1:
        selected_student = st.selectbox(
            "Select Student",
            options=list(st.session_state.system.students.keys()),
            key="registration_student",
        )
    with col2:
        selected_event_reg = st.selectbox(
            "Select Event",
            options=list(st.session_state.system.events.keys()),
            key="registration_event",
        )

    if st.button("Register"):
        registration = st.session_state.system.register_for_event(
            selected_student, selected_event_reg
        )
        if registration:
            st.success(f"Registration successful! Status: {registration.status.value}")
        else:
            st.error("Registration failed!")


def manage_events():
    """
    Handle all event management operations in the application.

    This function provides a complete interface for event management:
    - Create new events with conflict detection
    - List and display all current events
    - Show event details including registration status and capacity
    - Register students for events

    Features:
        - Automatic conflict detection for time and venue
        - Interactive form for event creation
        - Visual representation of event status
        - Conflict warnings and resolution options

    Dependencies:
        - st.session_state.system: Instance of CampusEventManagementSystem

    Returns:
        None. Updates the Streamlit UI directly.
    """
    st.header("📅 Event Management")

    # Render UI components
    _render_add_event_form()
    _render_events_list()

    if st.session_state.system.events:
        _render_event_details()
        _render_registration_form()
