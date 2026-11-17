"""
Authentication Routes Controller
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_session
from app.models.user import User, Student, Faculty, Class, Department
from app.services.auth_service import authenticate_user, login_user_session, logout_user_session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash("Please enter both username and password.", "danger")
            return render_template('auth/login.html')

        user = authenticate_user(username, password)
        if user:
            login_user_session(user)
            flash(f"Welcome back, {session.get('name', user.username)}!", "success")

            # Route to respective role-based dashboard
            if user.role == 'faculty':
                return redirect(url_for('faculty.dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('auth.login'))
        else:
            flash("Invalid credentials. Please verify your username and password.", "danger")

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    db = get_session()
    classes = db.query(Class).all()
    departments = db.query(Department).all()

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'student')
        name = request.form.get('name', '').strip()

        # Validation
        if not username or not email or not password or not name:
            flash("All mandatory fields must be completed.", "danger")
            return render_template('auth/register.html', classes=classes, departments=departments)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/register.html', classes=classes, departments=departments)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('auth/register.html', classes=classes, departments=departments)

        # Check existing user
        if db.query(User).filter((User.username == username) | (User.email == email)).first():
            flash("A user with this username or email already exists.", "warning")
            return render_template('auth/register.html', classes=classes, departments=departments)

        # Create User
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        db.add(new_user)
        db.flush()

        if role == 'student':
            roll_no = request.form.get('roll_no', '').strip()
            class_id = request.form.get('class_id')
            if not roll_no or not class_id:
                db.rollback()
                flash("Roll number and Class selection are required for student accounts.", "danger")
                return render_template('auth/register.html', classes=classes, departments=departments)

            student_profile = Student(user_id=new_user.user_id, class_id=int(class_id), roll_no=roll_no, name=name)
            db.add(student_profile)

        elif role == 'faculty':
            dept_id = request.form.get('dept_id')
            if not dept_id:
                db.rollback()
                flash("Department selection is required for faculty accounts.", "danger")
                return render_template('auth/register.html', classes=classes, departments=departments)

            faculty_profile = Faculty(user_id=new_user.user_id, dept_id=int(dept_id), name=name)
            db.add(faculty_profile)

        db.commit()
        flash("Registration successful! You may now log in with your credentials.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', classes=classes, departments=departments)

@auth_bp.route('/logout')
def logout():
    logout_user_session()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('auth.login'))
