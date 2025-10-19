import pandas as pd
import plotly.express as px
import streamlit as st

from models import RegistrationStatus


def dashboard():
    """
    Render the main dashboard tab of the application.

    This function creates the primary dashboard view with key statistics and visualizations:
    - Display key metrics (total students, events, and active service requests)
    - Show event status overview with interactive charts
    - Visualize registration statistics for all events

    Dependencies:
        - st.session_state.system: Instance of CampusEventManagementSystem
        - plotly.express: For interactive charts
        - pandas: For data manipulation

    Returns:
        None. Updates the Streamlit UI directly.
    """
    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Students", len(st.session_state.system.students))
    with col2:
        st.metric("Total Events", len(st.session_state.system.events))
    with col3:
        st.metric(
            "Active Service Requests", len(st.session_state.system.service_requests)
        )

    st.subheader("Event Status Overview")
    event_data = []
    for event in st.session_state.system.events.values():
        confirmed = sum(
            1
            for reg in event.registrations
            if reg.status == RegistrationStatus.CONFIRMED
        )
        waitlisted = sum(
            1
            for reg in event.registrations
            if reg.status == RegistrationStatus.WAITLISTED
        )
        event_data.append(
            {
                "Event": event.title,
                "Total Seats": event.max_seats,
                "Confirmed": confirmed,
                "Waitlisted": waitlisted,
                "Available": event.max_seats - confirmed,
            }
        )

    if event_data:
        df = pd.DataFrame(event_data)
        fig = px.bar(
            df,
            x="Event",
            y=["Confirmed", "Waitlisted", "Available"],
            title="Event Registration Status",
            barmode="stack",
        )
        st.plotly_chart(fig)
