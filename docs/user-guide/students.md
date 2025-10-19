# Student Management - User Guide

Complete guide to managing students in the Campus Event & Student Service Management System.

## Overview

The Student Management module allows you to:

- ✅ Add, edit, and delete student records
- 📋 View all registered students
- 🔍 Search and filter students
- 📊 Track student event registrations
- 📝 Monitor service requests per student
- 📤 Export student data

## Accessing Student Management

1. Launch the application: `http://localhost:8501`
2. Click **"Manage Students"** in the left sidebar
3. The Student Management interface will open

## Adding a New Student

### Step-by-Step Guide

1. **Navigate** to the "Add New Student" section (usually in an expander)
2. **Fill in** the required fields:
   - **Student ID**: Unique identifier (e.g., "STU001")
   - **Name**: Full name of the student
   - **Email**: Contact email address
   - **Major**: Field of study or department
3. **Click** the "Add Student" button
4. **Confirmation**: You'll see a success message

### Student ID Best Practices

!!! tip "ID Format Recommendations"
    - Use consistent format: `STU001`, `STU002`, etc.
    - IDs are **case-sensitive**
    - Keep them short but meaningful
    - Avoid special characters (stick to letters and numbers)

### Required Fields

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| Student ID | ✅ Yes | Alphanumeric | STU001 |
| Name | ✅ Yes | Text | Alice Johnson |
| Email | ✅ Yes | Valid email | alice@college.edu |
| Major | ✅ Yes | Text | Computer Science |

### Example Entry

```
Student ID: STU001
Name: Alice Johnson
Email: alice.johnson@college.edu
Major: Computer Science
```

## Viewing Students

### Student List

The main view displays all registered students in a table format:

| Student ID | Name | Email | Major | Registrations | Service Requests |
|------------|------|-------|-------|---------------|------------------|
| STU001 | Alice Johnson | alice@college.edu | Computer Science | 3 | 1 |
| STU002 | Bob Smith | bob@college.edu | Mathematics | 2 | 0 |

### Information Displayed

- **Student ID**: Unique identifier
- **Name**: Full name
- **Email**: Contact information
- **Major**: Field of study
- **Registrations**: Number of events registered
- **Service Requests**: Number of service requests

## Student Details

### Viewing Detailed Information

1. **Select** a student from the dropdown menu
2. **View** comprehensive information:
   - Basic student information
   - List of registered events
   - Event registration status (Confirmed/Waitlisted)
   - All service requests
   - Request status and priority

### Event Registrations

For each student, you can see:

- **Event Name**: Which events they're registered for
- **Event Date**: When the event takes place
- **Registration Status**: 
  - ✅ **Confirmed**: Successfully registered
  - ⏳ **Waitlisted**: On the waiting list
  - ❌ **Cancelled**: Registration cancelled

### Service Requests

View all service requests made by the student:

- **Request ID**: Unique identifier
- **Service Type**: Category (IT Support, Library Access, etc.)
- **Description**: What the student needs
- **Status**: Pending, In Progress, Completed, Rejected
- **Priority**: High, Medium, Low
- **Submitted Date**: When the request was made

## Editing Student Information

!!! note "Edit Functionality"
    Currently, to edit student information, you may need to delete and re-add the student. Future versions will include direct editing capability.

## Deleting Students

!!! warning "Delete Warning"
    Deleting a student will also remove all their event registrations and service requests. This action cannot be undone.

### How to Delete

1. Select the student to delete
2. Look for a "Delete Student" button (if available)
3. Confirm the deletion
4. The student and all associated data will be removed

## Searching and Filtering

### Search by ID
Use the student selector dropdown to quickly find a student by their ID.

### Filter by Major
Some views allow filtering students by their major/department.

### Sort Students
Click column headers to sort the student list alphabetically or by other criteria.

## Exporting Student Data

Export student information for external use:

1. **Navigate** to the student list
2. **Click** the export button (usually above or below the table)
3. **Choose format**: CSV or Excel
4. **Download** the file

### Export Use Cases

- 📊 Creating reports
- 📧 Email lists
- 📁 Backup purposes
- 📈 External analysis

## Common Operations

### Bulk Operations

#### Add Multiple Students
```python
# Example batch of students to add
students = [
    {"id": "STU001", "name": "Alice Johnson", "email": "alice@college.edu", "major": "CS"},
    {"id": "STU002", "name": "Bob Smith", "email": "bob@college.edu", "major": "Math"},
    {"id": "STU003", "name": "Carol Williams", "email": "carol@college.edu", "major": "Physics"},
]
```

#### Import from CSV
Future feature: Import students from CSV file.

## Integration with Other Modules

### Event Registration

From the Student Management page, you can:
- See which events a student is registered for
- View registration status
- Access event details

### Service Requests

Monitor all service requests by student:
- Track pending requests
- View request history
- See resolution status

## Analytics Integration

Student data feeds into the Analytics module:

- 📊 Student distribution by major
- 📈 Event participation rates per student
- 🎯 Most active students
- 📉 Service request patterns

## Validation Rules

The system validates student data:

✅ **Valid Inputs**
- Unique student ID
- Valid email format
- Non-empty name and major

❌ **Invalid Inputs**
- Duplicate student ID
- Empty required fields
- Invalid email format
- Special characters in ID (depending on config)

## Error Messages

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| "Student ID already exists" | Duplicate ID | Use a different ID |
| "Invalid email format" | Email doesn't match pattern | Check email format |
| "Required field missing" | Empty field | Fill all required fields |
| "Student not found" | ID doesn't exist | Check the ID or add student first |

## Troubleshooting

### Student Not Appearing in List

1. Refresh the page (Ctrl+R)
2. Check if the student was actually added (look for success message)
3. Verify the student ID is correct

### Cannot Register Student for Event

1. Ensure the student exists in the system
2. Check if the event has available seats
3. Verify the student isn't already registered

### Export Not Working

1. Check browser pop-up settings
2. Ensure you have write permissions
3. Try a different browser

## Best Practices

!!! success "Tips for Success"
    - **Consistent Naming**: Use a standard format for student IDs
    - **Regular Backups**: Export student data periodically
    - **Data Validation**: Double-check information before adding
    - **Clean Data**: Remove inactive or duplicate students
    - **Monitor Activity**: Track student engagement through registrations

## Advanced Features

### Student Metrics

View student engagement metrics:
- Total events registered
- Average registration rate
- Service request frequency
- Popular event categories

### Waitlist Management

When events are full:
- Students are automatically placed on waitlist
- Track waitlist position
- Get notified when seats become available

## Privacy & Data Security

!!! info "Data Protection"
    - Student emails are stored securely
    - Access is controlled through the application
    - Export features should be used responsibly
    - Follow your institution's data privacy policies

## Related Documentation

- 📅 [Event Management](events.md) - Manage events and registrations
- 📝 [Service Requests](requests.md) - Handle student service requests
- 📊 [Analytics](analytics.md) - View student engagement analytics
- 🏠 [Dashboard](dashboard.md) - System overview

## Quick Reference Card

| Action | Steps |
|--------|-------|
| **Add Student** | Manage Students → Fill form → Add Student |
| **View Details** | Select student from dropdown |
| **Register for Event** | Events → Select student → Register |
| **Track Requests** | View student details → Service Requests section |
| **Export Data** | Student list → Export button → Choose format |

## Next Steps

Now that you understand student management:

1. ✅ [Learn Event Management](events.md)
2. ✅ [Handle Service Requests](requests.md)
3. ✅ [View Analytics Dashboard](analytics.md)
4. ✅ [Explore Advanced Features](../getting-started/configuration.md)

## Need Help?

- 📖 [Full Documentation](../index.md)
- ❓ [FAQ](../getting-started/quick-start.md#troubleshooting)
- 🐛 [Report Issues](https://github.com/0Tarun0709/Campus-Event-Student-Service-Management/issues)
- 💬 [Ask Questions](https://github.com/0Tarun0709/Campus-Event-Student-Service-Management/discussions)
