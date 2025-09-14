import streamlit as st
from models import RequestStatus, RegistrationStatus

def manage_service_requests():
    """
    Handle all service request operations in the application.
    
    This function provides a complete interface for service request management:
    - Submit new service requests
    - Track and update request status
    - Manage request lifecycle
    - View request history
    
    Features:
        - Service request submission form
        - Status tracking (Open → In-Progress → Resolved)
        - Category-based organization
        - Real-time status updates
        - Visual status indicators
    
    Request Categories:
        - Hostel Maintenance
        - Library Access
        - Counseling
        - Other
    
    Status Workflow:
        1. Open: Initial state of new requests
        2. In-Progress: Requests being processed
        3. Resolved: Completed requests
    
    Dependencies:
        - st.session_state.system: Instance of CampusEventManagementSystem
        - RequestStatus: Enum for request status values
    
    Returns:
        None. Updates the Streamlit UI directly.
    """
    st.header("🔧 Service Requests")
    

    with st.expander("Raise New Service Request"):
        col1, col2 = st.columns(2)
        with col1:
            request_id = st.text_input("Request ID")
            student_id = st.selectbox("Student ID", options=list(st.session_state.system.students.keys()))
        with col2:
            category = st.selectbox("Category", ["Hostel Maintenance", "Library Access", "Counseling", "Other"])
        
        if st.button("Submit Request"):
            if all([request_id, student_id, category]):
                request = st.session_state.system.raise_service_request(request_id, student_id, category)
                if request:
                    st.success("Service request submitted successfully!")
    

    st.subheader("Service Requests Management")
    if st.session_state.system.service_requests:

        for request in st.session_state.system.service_requests.values():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    st.text(f"ID: {request.request_id}\nStudent: {request.student.student_id}")
                with col2:
                    st.text(f"Category: {request.category}\nCreated: {request.created_at.strftime('%Y-%m-%d %H:%M')}")
                with col3:
                    current_status = request.status.value
                    new_status = st.selectbox(
                        "Status",
                        options=[status.value for status in RequestStatus],
                        key=f"status_{request.request_id}",
                        index=[status.value for status in RequestStatus].index(current_status)
                    )
                    if new_status != current_status:
                        st.session_state.system.update_service_request_status(
                            request.request_id,
                            RequestStatus(new_status)
                        )
                with col4:
                    status_color = {
                        "Open": "🔴",
                        "In-Progress": "🟡",
                        "Resolved": "🟢"
                    }
                    st.markdown(f"### {status_color.get(new_status, '⚪')}")
                st.divider()
    else:
        st.info("No service requests.")
