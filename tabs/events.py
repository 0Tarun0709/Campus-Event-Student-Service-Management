import streamlit as st
from models import RequestStatus, RegistrationStatus
import pandas as pd

def manage_events():
    """
    Handle all event management operations in the application.
    
    This function provides a complete interface for event management:
    - Create new events with conflict detection
    - List and display all current events
    - Show event details including:
        * Registration status
        * Capacity information
        * Scheduling conflicts
        * Venue allocation
    
    Features:
        - Automatic conflict detection for time and venue
        - Interactive form for event creation
        - Visual representation of event status
        - Conflict warnings and resolution options
    
    Dependencies:
        - st.session_state.system: Instance of CampusEventManagementSystem
        - datetime: For date and time handling
    
    Returns:
        None. Updates the Streamlit UI directly.
    """
    st.header("📅 Event Management")
    
    conflict_warning = "conflict_warning"
    add_anyway = "add_anyway"

    # Add new event section with conflict detection popup
    with st.expander("Add New Event"):
        col1, col2 = st.columns(2)
        with col1:
            event_id = st.text_input("Event ID")
            title = st.text_input("Event Title")
            club = st.text_input("Organizing Club")
            venue = st.text_input("Venue")
        with col2:
            date = st.date_input("Date")
            start_time = st.time_input("Start Time")
            end_time = st.time_input("End Time")
            max_seats = st.number_input("Maximum Seats", min_value=1, value=50)
        
        # Initialize session state flags if missing
        if conflict_warning not in st.session_state:
            st.session_state[conflict_warning] = False
        if add_anyway not in st.session_state:
            st.session_state[add_anyway] = False

        def reset_flags():
            st.session_state[conflict_warning] = False
            st.session_state[add_anyway] = False

        # Check conflicts for the new event against existing events
        def check_conflicts_new_event():
            # Temporary Event class to use existing conflict logic
            class TempEvent:
                def __init__(self, event_id, title, club, date, start_time, end_time, venue):
                    self.event_id = event_id
                    self.title = title
                    self.club = club
                    self.date = date.strftime("%Y-%m-%d")
                    self.start_time = start_time.strftime("%I:%M %p")
                    self.end_time = end_time.strftime("%I:%M %p")
                    self.venue = venue
                def get_conflict_details(self, other_event):
                    # Using system method for event conflict detection if available;
                    # fallback minimal logic could be implemented if needed.
                    if hasattr(st.session_state.system, 'get_event_conflict'):
                        return st.session_state.system.get_event_conflict(self, other_event)
                    else:
                        # Minimal time and venue conflict check:
                        conflict = {
                            "has_conflict": False,
                            "venue_conflict": False,
                            "time_conflict": False,
                            "conflict_period": {}
                        }
                        if self.venue == other_event.venue and self.date == other_event.date:
                            conflict["venue_conflict"] = True
                            # Check time overlap (simple string parse or convert to datetime)
                            from datetime import datetime
                            fmt = "%I:%M %p"
                            start1 = datetime.strptime(self.start_time, fmt)
                            end1 = datetime.strptime(self.end_time, fmt)
                            start2 = datetime.strptime(other_event.start_time, fmt)
                            end2 = datetime.strptime(other_event.end_time, fmt)
                            overlap = max(start1, start2) < min(end1, end2)
                            if overlap:
                                conflict["time_conflict"] = True
                                conflict["has_conflict"] = True
                                conflict["conflict_period"] = {
                                    "date": self.date,
                                    "start": max(start1, start2).strftime(fmt),
                                    "end": min(end1, end2).strftime(fmt),
                                }
                        conflict["has_conflict"] = conflict["venue_conflict"] or conflict["time_conflict"]
                        return conflict

            temp_event = TempEvent(event_id, title, club, date, start_time, end_time, venue)
            conflicts_list = []
            for other_event in st.session_state.system.events.values():
                if other_event.event_id != event_id:
                    conflict_details = temp_event.get_conflict_details(other_event)
                    if conflict_details["has_conflict"]:
                        conflict_desc = []
                        if conflict_details["venue_conflict"]:
                            conflict_desc.append(f"Venue conflict at {venue}")
                        if conflict_details["time_conflict"]:
                            period = conflict_details["conflict_period"]
                            conflict_desc.append(
                                f"Time overlap on {period['date']} between {period['start']} and {period['end']}"
                            )
                        conflicts_list.append(f"Conflicts with {other_event.title}: " + " AND ".join(conflict_desc))
            return conflicts_list

        if st.button("Add Event") or st.session_state[add_anyway]:
            if st.session_state[add_anyway]:
                reset_flags()
                st.session_state.system.add_event(
                    event_id=event_id,
                    title=title,
                    club=club,
                    date=date.strftime("%Y-%m-%d"),
                    start_time=start_time.strftime("%I:%M %p"),
                    end_time=end_time.strftime("%I:%M %p"),
                    venue=venue,
                    max_seats=max_seats
                )
                st.success("Event added successfully!")
            else:
                if all([event_id, title, club, venue]):
                    conflicts_found = check_conflicts_new_event()
                    if conflicts_found and not st.session_state[add_anyway]:
                        st.session_state[conflict_warning] = conflicts_found
                    else:
                        reset_flags()
                        st.session_state.system.add_event(
                            event_id=event_id,
                            title=title,
                            club=club,
                            date=date.strftime("%Y-%m-%d"),
                            start_time=start_time.strftime("%I:%M %p"),
                            end_time=end_time.strftime("%I:%M %p"),
                            venue=venue,
                            max_seats=max_seats
                        )
                        st.success("Event added successfully!")
                else:
                    st.error("Please fill in all required fields (Event ID, Title, Club, Venue).")

        # Show conflict warning popup with options
        if st.session_state[conflict_warning]:
            st.warning("Detected scheduling conflicts with this event:")
            for conflict_text in st.session_state[conflict_warning]:
                st.write(f"- {conflict_text}")
            colA, colB = st.columns(2)
            with colA:
                if st.button("Change Event"):
                    st.session_state[conflict_warning] = False
            with colB:
                if st.button("Add Anyway"):
                    st.session_state[add_anyway] = True
                    st.session_state.system.add_event(
                            event_id=event_id,
                            title=title,
                            club=club,
                            date=date.strftime("%Y-%m-%d"),
                            start_time=start_time.strftime("%I:%M %p"),
                            end_time=end_time.strftime("%I:%M %p"),
                            venue=venue,
                            max_seats=max_seats
                        )
                    st.success("Event added successfully!")
                    # st.experimental_rerun()


    st.subheader("Current Events")
    if st.session_state.system.events:
        event_data = []
        for event in st.session_state.system.events.values():
            summary = event.get_summary()
            

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
                        conflicts.append(f"Conflicts with {other_event.title}: " + " AND ".join(conflict_desc))
            
            event_data.append({
                "Event ID": event.event_id,
                "Title": event.title,
                "Date": event.date,
                "Time": f"{event.start_time} - {event.end_time}",
                "Venue": event.venue,
                "Available Seats": event.max_seats - summary['seats']['confirmed'],
                "Status": summary['status'],
                "Conflicts": "\\n".join(conflicts) if summary['status'] == "Invalid Schedule" else "No conflicts"
            })
        df = pd.DataFrame(event_data)
        st.dataframe(df)
        

        st.subheader("Event Details & Registrations")
        selected_event = st.selectbox(
            "Select Event to View Details",
            options=list(st.session_state.system.events.keys()),
            key="event_details"
        )
        
        if selected_event:
            event = st.session_state.system.events[selected_event]
            

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Seats", event.max_seats)
            with col2:
                confirmed = sum(1 for reg in event.registrations if reg.status == RegistrationStatus.CONFIRMED)
                st.metric("Confirmed Registrations", confirmed)
            with col3:
                waitlisted = sum(1 for reg in event.registrations if reg.status == RegistrationStatus.WAITLISTED)
                st.metric("Waitlisted", waitlisted)
            

            st.markdown("##### 👥 Registered Students")
            if event.registrations:
                registration_data = []
                for reg in event.registrations:
                    registration_data.append({
                        "Student ID": reg.student.student_id,
                        "Student Name": reg.student.name,
                        "Registration Status": reg.status.value,
                        "Other Registrations": len(reg.student.registrations) - 1,
                        "Service Requests": len(reg.student.service_requests)
                    })
                st.dataframe(pd.DataFrame(registration_data))
            else:
                st.info("No students registered for this event")
        

        st.subheader("Register for Event")
        col1, col2 = st.columns(2)
        with col1:
            selected_student = st.selectbox("Select Student", 
                                         options=list(st.session_state.system.students.keys()),
                                         key="registration_student")
        with col2:
            selected_event_reg = st.selectbox("Select Event", 
                                       options=list(st.session_state.system.events.keys()),
                                       key="registration_event")
        
        if st.button("Register"):
            registration = st.session_state.system.register_for_event(selected_student, selected_event_reg)
            if registration:
                st.success(f"Registration successful! Status: {registration.status.value}")
            else:
                st.error("Registration failed!")
    else:
        st.info("No events available.")
