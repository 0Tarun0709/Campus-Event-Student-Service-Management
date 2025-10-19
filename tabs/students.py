import pandas as pd
import streamlit as st

from models import RegistrationStatus


def manage_students():
    """
    Manage all student-related operations in the application.

    This function provides a comprehensive interface for student management:
    - Add new students to the system
    - View and manage student profiles
    - Track student event registrations
    - Monitor service requests

    Features:
        - Student registration form
        - Detailed student information display
        - Registration status tracking
        - Interactive student selection
        - Service request history

    Data Visualization:
        - Student registration summary
        - Event participation metrics
        - Service request statistics

    Dependencies:
        - st.session_state.system: Instance of CampusEventManagementSystem
        - pandas: For data organization and display

    Returns:
        None. Updates the Streamlit UI directly.
    """
    st.header("👥 Student Management")

    with st.expander("Add New Student"):
        student_id = st.text_input("Student ID")
        student_name = st.text_input("Student Name")
        if st.button("Add Student"):
            if student_id:
                st.session_state.system.add_student(student_id, student_name)
                st.success(f"Student {student_id} added successfully!")

    st.subheader("Student Management")
    if st.session_state.system.students:

        student_data = []
        for student in st.session_state.system.students.values():
            registrations = len(
                [
                    r
                    for r in student.registrations
                    if r.status == RegistrationStatus.CONFIRMED
                ]
            )
            waitlisted = len(
                [
                    r
                    for r in student.registrations
                    if r.status == RegistrationStatus.WAITLISTED
                ]
            )
            student_data.append(
                {
                    "Student ID": student.student_id,
                    "Student Name": student.name,
                    "Registered Events": registrations,
                    "Waitlisted Events": waitlisted,
                    "Service Requests": len(student.service_requests),
                }
            )
        df = pd.DataFrame(student_data)
        st.dataframe(df)

        st.subheader("Student Details")
        selected_student_id = st.selectbox(
            "Select Student to View Details",
            options=list(st.session_state.system.students.keys()),
        )

        if selected_student_id:
            student = st.session_state.system.students[selected_student_id]

            st.markdown("##### 📅 Registered Events")
            if student.registrations:
                event_data = []
                for reg in student.registrations:
                    event_data.append(
                        {
                            "Event": reg.event.title,
                            "Date": reg.event.date,
                            "Time": f"{reg.event.start_time} - {reg.event.end_time}",
                            "Venue": reg.event.venue,
                            "Status": reg.status.value,
                        }
                    )
                st.dataframe(pd.DataFrame(event_data))
            else:
                st.info("No event registrations")

            st.markdown("##### 🔧 Service Requests")
            if student.service_requests:
                request_data = []
                for req in student.service_requests:
                    request_data.append(
                        {
                            "Request ID": req.request_id,
                            "Category": req.category,
                            "Status": req.status.value,
                            "Created At": req.created_at.strftime("%Y-%m-%d %H:%M"),
                        }
                    )
                st.dataframe(pd.DataFrame(request_data))
            else:
                st.info("No service requests")
    else:
        st.info("No students registered yet.")
