import streamlit as st
# from models import RequestStatus, RegistrationStatus
import pandas as pd
import plotly.express as px

def reports_analytics():
    """
    Generate and display comprehensive analytics and reports for the system.
    
    This function creates interactive visualizations and reports for:
    - Event Analytics
        * Registration distribution
        * Venue utilization
        * Capacity analysis
        * Event popularity metrics
    
    - Service Request Analytics
        * Status distribution
        * Category analysis
        * Resolution metrics
        * Trend analysis
    
    Visualizations:
        1. Event Registration Distribution
           - Stacked bar chart showing confirmed/waitlisted/available seats
        
        2. Venue Usage Analysis
           - Pie chart showing event distribution across venues
        
        3. Service Request Status
           - Pie chart showing request status distribution
        
        4. Category Distribution
           - Pie chart showing service request categories
    
    Dependencies:
        - st.session_state.system: Instance of CampusEventManagementSystem
        - plotly.express: For interactive charts
        - pandas: For data processing
    
    Returns:
        None. Updates the Streamlit UI with interactive charts and metrics.
    """
    st.header("📈 Reports & Analytics")
    

    st.subheader("Event Analytics")
    if st.session_state.system.events:

        registration_data = []
        for event in st.session_state.system.events.values():
            summary = event.get_summary()
            registration_data.append({
                'Event': event.title,
                'Confirmed': summary['seats']['confirmed'],
                'Waitlisted': summary['seats']['waitlisted'],
                'Available': event.max_seats - summary['seats']['confirmed']
            })
        df_reg = pd.DataFrame(registration_data)
        fig_reg = px.bar(df_reg, x='Event', y=['Confirmed', 'Waitlisted', 'Available'],
                        title='Registration Distribution by Event', barmode='stack')
        st.plotly_chart(fig_reg)
        

        venue_usage = {}
        for event in st.session_state.system.events.values():
            venue_usage[event.venue] = venue_usage.get(event.venue, 0) + 1
        fig_venue = px.pie(values=list(venue_usage.values()), names=list(venue_usage.keys()),
                          title='Event Distribution by Venue')
        st.plotly_chart(fig_venue)
    

    st.subheader("Service Request Analytics")
    if st.session_state.system.service_requests:

        status_summary = st.session_state.system.get_service_request_summary()
        fig_status = px.pie(values=list(status_summary.values()), names=list(status_summary.keys()),
                           title='Service Requests by Status')
        st.plotly_chart(fig_status)
        

        category_dist = {}
        for request in st.session_state.system.service_requests.values():
            category_dist[request.category] = category_dist.get(request.category, 0) + 1
        fig_category = px.pie(values=list(category_dist.values()), names=list(category_dist.keys()),
                            title='Service Requests by Category')
        st.plotly_chart(fig_category)
