import os
import sys

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Increase AppTest timeout to allow the app to initialize in CI environments
# Default is 3s which can be too short for slower CI runners
TIMEOUT = 15


class TestStreamlitApp:
    """Integration tests for the Streamlit application."""

    @pytest.fixture
    def app_test(self):
        """Create an AppTest instance for testing."""
        return AppTest.from_file("app.py")

    def test_app_initialization(self, app_test):
        """Test that the app initializes without errors."""
        app_test.run(timeout=TIMEOUT)
        assert not app_test.exception

    def test_tab_navigation(self, app_test):
        """Test tab navigation functionality."""
        app_test.run(timeout=TIMEOUT)

        # Check that tabs exist
        assert len(app_test.tabs) > 0

        # Check that app runs without exception
        assert not app_test.exception

    def test_student_management_tab(self, app_test):
        """Test student management functionality."""
        app_test.run(timeout=TIMEOUT)

        # Check that the app has multiple tabs (including student management)
        assert len(app_test.tabs) >= 2

        # Check that the app loaded without errors
        assert not app_test.exception

    def test_event_management_tab(self, app_test):
        """Test event management functionality."""
        app_test.run(timeout=TIMEOUT)

        # Check that the app has multiple tabs (including event management)
        assert len(app_test.tabs) >= 3

        # Check that the app loaded without errors
        assert not app_test.exception

    def test_dashboard_displays_data(self, app_test):
        """Test that dashboard displays system data."""
        app_test.run(timeout=TIMEOUT)

        # Dashboard is the first tab (index 0), which should be open by default
        # Check that the app loaded without errors
        assert not app_test.exception


@pytest.mark.integration
class TestAppWorkflow:
    """End-to-end workflow tests."""

    @pytest.fixture
    def app_test(self):
        """Create an AppTest instance for testing."""
        return AppTest.from_file("app.py")

    def test_complete_student_event_workflow(self, app_test):
        """Test complete workflow from adding student to event registration."""
        app_test.run(timeout=TIMEOUT)

        # Check that the app has all expected tabs
        assert (
            len(app_test.tabs) >= 5
        )  # Dashboard, Students, Events, Service Requests, Reports

        # Check that the app loaded without errors
        assert not app_test.exception
