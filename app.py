import streamlit as st
from main import CampusEventManagementSystem
from tabs.analytics import reports_analytics
from tabs.dashboard import dashboard
from tabs.events import manage_events
from tabs.requests import manage_service_requests
from tabs.students import manage_students


from data.data import students, events, registrations, service_requests

# Initialize the system in session state if not exists
if 'system' not in st.session_state:
    st.session_state.system = CampusEventManagementSystem()

def init_sample_data():
    """Initialize sample data if not already present"""
    system = st.session_state.system
    

    if not system.students:
        for sid in students:
            system.add_student(sid)
    

    if not system.events:
        for event in events:
            system.add_event(**event)
        

        for student_id, event_id in registrations:
            system.register_for_event(student_id, event_id)
        

        for request_id, student_id, category in service_requests:
            system.raise_service_request(request_id, student_id, category)

def main():
    st.set_page_config(page_title="Campus Event Management System", 
                       page_icon="🎓", 
                       layout="wide")
    
    st.title("🎓 Campus Event & Student Service Management")
    

    init_sample_data()
    

    tabs = st.tabs(["Dashboard", "Students", "Events", "Service Requests", "Reports"])
    
    with tabs[0]:
        dashboard()
    with tabs[1]:
        manage_students()
    with tabs[2]:
        manage_events()
    with tabs[3]:
        manage_service_requests()
    with tabs[4]:
        reports_analytics()

if __name__ == "__main__":
    main()
