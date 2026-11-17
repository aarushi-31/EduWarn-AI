-- ==============================================================================
-- Database Schema: AI-Based Student Performance Prediction & Early Warning System
-- Conforms strictly to Experiment 5 (3NF Normalized Relational Schema)
-- JSS University, Noida | Dept of CSE (AIML)
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- 1. USER
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'faculty', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. DEPARTMENT
CREATE TABLE IF NOT EXISTS departments (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    hod_id INTEGER,
    FOREIGN KEY (hod_id) REFERENCES faculty(faculty_id) ON DELETE SET NULL
);

-- 3. CLASS
CREATE TABLE IF NOT EXISTS classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL,
    section VARCHAR(10) NOT NULL,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    academic_year VARCHAR(20) NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE RESTRICT
);

-- 4. FACULTY
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    dept_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE RESTRICT
);

-- 5. STUDENT
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    class_id INTEGER NOT NULL,
    roll_no VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE RESTRICT
);

-- 6. SUBJECT
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL,
    subject_code VARCHAR(20) NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE RESTRICT
);

-- 7. TEACHING_ASSIGNMENT
CREATE TABLE IF NOT EXISTS teaching_assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE RESTRICT,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE RESTRICT,
    CONSTRAINT uq_teaching_assignment UNIQUE (faculty_id, subject_id, class_id)
);

-- 8. ASSESSMENT_CYCLE
CREATE TABLE IF NOT EXISTS assessment_cycles (
    cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_name VARCHAR(50) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- 9. ACADEMIC_RECORD
CREATE TABLE IF NOT EXISTS academic_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    cycle_id INTEGER NOT NULL,
    entered_by INTEGER NOT NULL,
    attendance_pct REAL NOT NULL CHECK (attendance_pct >= 0 AND attendance_pct <= 100),
    internal_marks REAL NOT NULL CHECK (internal_marks >= 0),
    assignment_score REAL NOT NULL CHECK (assignment_score >= 0),
    participation_score REAL NOT NULL CHECK (participation_score >= 0),
    prev_sem_marks REAL NOT NULL CHECK (prev_sem_marks >= 0 AND prev_sem_marks <= 100),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE RESTRICT,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE RESTRICT,
    FOREIGN KEY (cycle_id) REFERENCES assessment_cycles(cycle_id) ON DELETE RESTRICT,
    FOREIGN KEY (entered_by) REFERENCES faculty(faculty_id) ON DELETE RESTRICT,
    CONSTRAINT uq_student_subject_cycle UNIQUE (student_id, subject_id, cycle_id)
);

-- 10. ML_MODEL
CREATE TABLE IF NOT EXISTS ml_models (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm VARCHAR(80) NOT NULL,
    version VARCHAR(20) NOT NULL,
    accuracy REAL NOT NULL,
    f1_score REAL NOT NULL,
    trained_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. PREDICTION
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    cycle_id INTEGER NOT NULL,
    model_id INTEGER NOT NULL,
    risk_category VARCHAR(20) NOT NULL CHECK (risk_category IN ('Low', 'Medium', 'High')),
    risk_score REAL NOT NULL,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE RESTRICT,
    FOREIGN KEY (cycle_id) REFERENCES assessment_cycles(cycle_id) ON DELETE RESTRICT,
    FOREIGN KEY (model_id) REFERENCES ml_models(model_id) ON DELETE RESTRICT,
    CONSTRAINT uq_student_cycle_model UNIQUE (student_id, cycle_id, model_id)
);

-- 12. PREDICTION_FACTOR
CREATE TABLE IF NOT EXISTS prediction_factors (
    factor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER NOT NULL,
    feature_name VARCHAR(80) NOT NULL,
    contribution REAL NOT NULL,
    FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id) ON DELETE CASCADE
);

-- 13. SUGGESTION
CREATE TABLE IF NOT EXISTS suggestions (
    suggestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER NOT NULL,
    suggestion_text TEXT NOT NULL,
    FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id) ON DELETE CASCADE
);

-- 14. NOTIFICATION
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    prediction_id INTEGER,
    message TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT 0 CHECK (is_read IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id) ON DELETE CASCADE
);
