"""
Integration Tests for APIs and Admin / HOD Aggregates (FR8, FR11)
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import pytest

def test_admin_dashboard_and_reports(client):
    """Verify HOD / Admin can access department overview and printable reports."""
    # Log in as Admin
    client.post('/auth/login', data={'username': 'test_admin', 'password': 'AdminPass123!'}, follow_redirects=True)

    # 1. HOD Dashboard
    resp = client.get('/admin/dashboard')
    assert resp.status_code == 200
    assert b"Department Head Overview" in resp.data

    # 2. HOD Reports
    rep_resp = client.get('/admin/reports')
    assert rep_resp.status_code == 200
    assert b"Department Academic Report" in rep_resp.data

def test_api_unread_notifications_count(client):
    """Verify notification count endpoint returns JSON."""
    client.post('/auth/login', data={'username': 'test_student1', 'password': 'StudentPass123!'}, follow_redirects=True)

    resp = client.get('/api/notifications/unread-count')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'unread_count' in data

def test_api_department_risk_chart(client):
    """Verify department risk chart endpoint returns structured risk categories."""
    client.post('/auth/login', data={'username': 'test_admin', 'password': 'AdminPass123!'}, follow_redirects=True)

    resp = client.get('/api/charts/department-risk')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'labels' in data
    assert 'data' in data
    assert len(data['labels']) == 3

def test_api_student_metrics_history(client):
    """Verify student history chart endpoint returns cycle progression."""
    client.post('/auth/login', data={'username': 'test_student1', 'password': 'StudentPass123!'}, follow_redirects=True)

    resp = client.get('/api/charts/student-metrics/1')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'cycles' in data
    assert 'attendance' in data
    assert 'internals' in data
