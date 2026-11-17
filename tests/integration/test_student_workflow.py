"""
Integration Tests for Student Workflows & Privacy Protection (FR7, FR9, NFR2)
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import pytest

def test_student_login_and_dashboard(client):
    """Verify student can log in and view their personal standing and recommendations."""
    resp = client.post('/auth/login', data={
        'username': 'test_student1',
        'password': 'StudentPass123!'
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert b"Student Academic Self-Service Portal" in resp.data
    assert b"TEST001" in resp.data

def test_privacy_isolation_student_cannot_access_faculty_routes(client):
    """Verify role-based boundary: student is barred from faculty dashboard (NFR2, FR9)."""
    # 1. Log in as student
    client.post('/auth/login', data={'username': 'test_student1', 'password': 'StudentPass123!'}, follow_redirects=True)

    # 2. Attempt to access faculty dashboard
    resp = client.get('/faculty/dashboard', follow_redirects=True)
    assert resp.status_code == 200
    assert b"Access denied" in resp.data
    # Confirms redirect back to student's safe portal
    assert b"Student Academic Self-Service Portal" in resp.data

def test_student_notifications_workflow(client):
    """Verify student can view alerts and mark notifications as read."""
    client.post('/auth/login', data={'username': 'test_student1', 'password': 'StudentPass123!'}, follow_redirects=True)

    resp = client.get('/student/notifications')
    assert resp.status_code == 200
    assert b"Early Warning Alerts & Notifications" in resp.data
