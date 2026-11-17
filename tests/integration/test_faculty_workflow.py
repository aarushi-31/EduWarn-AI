"""
Integration Tests for Faculty Workflows (FR2, FR6, FR10)
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import io
import pytest

def test_faculty_login_and_dashboard_access(client):
    """Verify faculty can log in and access the faculty dashboard."""
    # 1. Login
    resp = client.post('/auth/login', data={
        'username': 'test_faculty',
        'password': 'FacultyPass123!'
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Faculty Academic Monitoring" in resp.data

    # 2. Access dashboard
    dash_resp = client.get('/faculty/dashboard')
    assert dash_resp.status_code == 200
    assert b"Student Academic Cohort" in dash_resp.data

def test_filter_students_by_risk(client):
    """Verify filtering student roster by risk category query parameters."""
    client.post('/auth/login', data={'username': 'test_faculty', 'password': 'FacultyPass123!'}, follow_redirects=True)

    # Filter High Risk
    resp = client.get('/faculty/dashboard?risk=High')
    assert resp.status_code == 200

    # Filter Low Risk
    resp_low = client.get('/faculty/dashboard?risk=Low')
    assert resp_low.status_code == 200

def test_enter_academic_record_form(client):
    """Verify faculty submitting marks for a student triggers database update and prediction."""
    client.post('/auth/login', data={'username': 'test_faculty', 'password': 'FacultyPass123!'}, follow_redirects=True)

    post_resp = client.post('/faculty/enter-record', data={
        'student_id': 1,
        'subject_id': 1,
        'cycle_id': 2,
        'attendance_pct': '68.0',
        'internal_marks': '18.0',
        'assignment_score': '15.0',
        'participation_score': '12.0',
        'prev_sem_marks': '62.0'
    }, follow_redirects=True)

    assert post_resp.status_code == 200
    assert b"Academic record successfully saved" in post_resp.data

def test_csv_bulk_upload_workflow(client):
    """Verify batch upload parses CSV and runs predictions."""
    client.post('/auth/login', data={'username': 'test_faculty', 'password': 'FacultyPass123!'}, follow_redirects=True)

    csv_data = (
        b"roll_no,attendance_pct,internal_marks,assignment_score,participation_score,prev_sem_marks\n"
        b"TEST001,55.0,12.0,10.0,8.0,50.0\n"
        b"TEST002,91.0,27.0,23.0,18.0,85.0\n"
    )

    resp = client.post('/faculty/upload-csv', data={
        'subject_id': 1,
        'cycle_id': 1,
        'csv_file': (io.BytesIO(csv_data), 'test_cohort.csv')
    }, content_type='multipart/form-data', follow_redirects=True)

    assert resp.status_code == 200
    assert b"Successfully processed 2 records" in resp.data
