"""
Authentication and Role-Based Access Control (RBAC) Service
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

from functools import wraps
from flask import session, redirect, url_for, flash, request, abort, g
from app.db import get_session
from app.models.user import User, Student, Faculty

def authenticate_user(username_or_email, password):
    """
    Verifies user credentials.
    Returns User object if successful, None otherwise.
    """
    db = get_session()
    user = db.query(User).filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if user and user.check_password(password):
        return user
    return None

def login_user_session(user):
    """Stores user information in Flask session."""
    session.clear()
    session['user_id'] = user.user_id
    session['username'] = user.username
    session['role'] = user.role
    session['email'] = user.email

    # Store role-specific IDs if available
    if user.role == 'student' and user.student_profile:
        session['student_id'] = user.student_profile.student_id
        session['name'] = user.student_profile.name
        session['roll_no'] = user.student_profile.roll_no
    elif user.role == 'faculty' and user.faculty_profile:
        session['faculty_id'] = user.faculty_profile.faculty_id
        session['name'] = user.faculty_profile.name
    elif user.role == 'admin':
        session['name'] = "Administrator / HOD"

def logout_user_session():
    """Clears current user session."""
    session.clear()

def get_current_user():
    """Retrieves current authenticated User from database based on session."""
    if 'user_id' not in session:
        return None
    db = get_session()
    return db.query(User).filter_by(user_id=session['user_id']).first()

def login_required(f):
    """Decorator requiring active authenticated session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    """Decorator restricting route access to specific user roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('auth.login', next=request.url))

            user_role = session.get('role')
            if user_role not in allowed_roles:
                flash("Access denied: You do not possess the required permissions for this resource.", "danger")
                # Redirect to appropriate home dashboard
                if user_role == 'faculty':
                    return redirect(url_for('faculty.dashboard'))
                elif user_role == 'student':
                    return redirect(url_for('student.dashboard'))
                elif user_role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
