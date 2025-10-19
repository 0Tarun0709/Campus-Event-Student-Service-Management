"""
Health check utilities for the Campus Management System.
"""

import sys
import time
from datetime import datetime
from typing import Any, Dict

import psutil
import streamlit as st


def get_system_health() -> Dict[str, Any]:
    """
    Get comprehensive system health information.

    Returns:
        Dict containing system health metrics
    """
    try:
        # Basic system info
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": time.time(),
            "python_version": sys.version,
        }

        # Memory usage
        memory = psutil.virtual_memory()
        health_data["memory"] = {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used,
        }

        # CPU usage
        health_data["cpu"] = {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
        }

        # Disk usage
        disk = psutil.disk_usage("/")
        health_data["disk"] = {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": (disk.used / disk.total) * 100,
        }

        # Application specific checks
        if "system" in st.session_state:
            system = st.session_state.system
            health_data["application"] = {
                "students_count": len(system.students),
                "events_count": len(system.events),
                "registrations_count": len(system.registrations),
                "service_requests_count": len(system.service_requests),
            }

        return health_data

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def health_check_page():
    """
    Streamlit page for health check endpoint.
    This can be accessed at /healthz when running the app.
    """
    st.set_page_config(page_title="Health Check", page_icon="🏥", layout="centered")

    st.title("🏥 System Health Check")

    # Get health data
    health_data = get_system_health()

    # Display status
    if health_data["status"] == "healthy":
        st.success("✅ System is healthy")
    else:
        st.error("❌ System is unhealthy")
        st.error(f"Error: {health_data.get('error', 'Unknown error')}")

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    if health_data["status"] == "healthy":
        with col1:
            st.metric(
                "Memory Usage",
                f"{health_data['memory']['percent']:.1f}%",
                delta=f"{health_data['memory']['available'] / (1024**3):.1f}GB available",
            )

        with col2:
            st.metric(
                "CPU Usage",
                f"{health_data['cpu']['percent']:.1f}%",
                delta=f"{health_data['cpu']['count']} cores",
            )

        with col3:
            st.metric(
                "Disk Usage",
                f"{health_data['disk']['percent']:.1f}%",
                delta=f"{health_data['disk']['free'] / (1024**3):.1f}GB free",
            )

        with col4:
            if "application" in health_data:
                st.metric(
                    "Total Students", health_data["application"]["students_count"]
                )

    # Detailed information in expander
    with st.expander("Detailed Health Information"):
        st.json(health_data)

    # Return health data for API access
    return health_data


if __name__ == "__main__":
    health_check_page()
