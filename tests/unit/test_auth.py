"""
Unit Tests for Authentication and Security (FR1, NFR1)
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import pytest
from app.models.user import User
from app.services.auth_service import authenticate_user

def test_password_hashing_security():
    """Verify that user passwords are encrypted using strong PBKDF2/SHA256 hashes and never stored in plaintext."""
    u = User(username='se_test_user', email='se@test.edu', role='student')
    plaintext_pass = 'SecretPass123!'
    u.set_password(plaintext_pass)

    assert u.password_hash != plaintext_pass
    assert u.password_hash.startswith('scrypt:') or u.password_hash.startswith('pbkdf2:')
    assert u.check_password(plaintext_pass) is True
    assert u.check_password('WrongPass') is False

def test_user_authentication_success(session):
    """Verify authenticating valid credentials returns the correct user entity."""
    user = authenticate_user('test_faculty', 'FacultyPass123!')
    assert user is not None
    assert user.username == 'test_faculty'
    assert user.role == 'faculty'

def test_user_authentication_invalid_password(session):
    """Verify authentication fails cleanly on invalid password."""
    user = authenticate_user('test_faculty', 'WrongPassword123')
    assert user is None

def test_user_authentication_nonexistent_user(session):
    """Verify authentication fails for non-existent username."""
    user = authenticate_user('ghost_user_999', 'AnyPass')
    assert user is None

def test_role_checks(session):
    """Verify correct assignment of student and faculty roles."""
    student = session.query(User).filter_by(username='test_student1').first()
    faculty = session.query(User).filter_by(username='test_faculty').first()
    admin = session.query(User).filter_by(username='test_admin').first()

    assert student.role == 'student'
    assert faculty.role == 'faculty'
    assert admin.role == 'admin'
