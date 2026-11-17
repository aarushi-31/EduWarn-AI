# Software Development Plan
## AI-Based Student Performance Prediction and Early Warning System
**Institution**: JSS University, Noida  
**Department**: Computer Science and Engineering (Artificial Intelligence & Machine Learning)  
**Academic Year**: 2026–2027 | **Semester**: 5th Semester B.Tech  
**Subject**: Software Engineering Laboratory (JCSAIMLL-001)

---

## 1. Project Understanding

In higher education institutions, academic monitoring has traditionally relied on manual assessment reviews after end-semester or mid-term examinations. By that time, struggling students have frequently fallen too far behind to recover. 

The **AI-Based Student Performance Prediction and Early Warning System** is an intelligent decision-support platform designed to solve this issue. By leveraging supervised machine learning on continuous academic indicators—such as attendance percentage, internal examination marks, assignment scores, classroom participation, and previous semester performance—the platform classifies students into three distinct risk categories:
- **Low Risk**: Student is academically on track; maintains high performance.
- **Medium Risk**: Student exhibits early warning indicators (e.g., dipping attendance, uneven test marks); needs targeted attention.
- **High Risk**: Student is in severe academic danger; requires urgent faculty counseling and remedial intervention.

### Core Philosophy: Decision Support, Not Decision Replacement
As defined in Experiment 1 and the Project SRS (Experiment 2), the system does **not** automate grading, punitive measures, or academic disciplinary decisions. It functions as an explainable, transparent early-warning advisor to faculty, academic heads (HOD), and students themselves.

---

## 2. Functional Requirements (FR1 – FR11)

| Requirement ID | Name | Description |
|---|---|---|
| **FR1** | User Authentication & Authorization | Secure user registration and login with password hashing. Supports three roles: Student, Faculty, and Admin/HOD. |
| **FR2** | Academic Data Entry & Upload | Faculty can enter single student records or upload batch CSV files containing attendance, internal marks, assignments, participation, and previous marks. |
| **FR3** | Data Preprocessing & Validation | Validates input ranges (e.g., attendance 0–100, marks >= 0), handles missing values, and prepares normalized feature vectors. |
| **FR4** | ML Risk Classification | Predicts a student's risk category (`Low`, `Medium`, `High`) and calculates a continuous risk score using a trained ML pipeline. |
| **FR5** | Factor Explainability | Calculates and displays key contributing factors (e.g., "Low attendance contributing +45% to risk"). |
| **FR6** | Faculty Risk-Filtered Dashboard | Faculty dashboard listing assigned students with real-time filtering by risk category (All, High, Medium, Low) and search by roll number/name. |
| **FR7** | Student Self-Service Dashboard | Authenticated student portal showing own performance records, current risk status, key factors, and personalized academic improvement tips. |
| **FR8** | Admin / HOD Aggregate Analytics | Department-wide and class-level summary statistics, risk distribution charts, and multi-cycle performance trends. |
| **FR9** | Role-Based Data Scoping (RBAC) | Strict access control: students see only their personal record; faculty see only their assigned classes/subjects; admin/HOD sees aggregate and departmental data. |
| **FR10** | Cycle-Based Prediction Versioning | Tracks predictions across academic assessment cycles (e.g., IA-1, IA-2, Pre-University Exam) to visualize student progress or regression over time. |
| **FR11** | Reporting & Export | Generates downloadable/printable academic summary reports and CSV exports for departmental meetings. |
| **Elicited** | Risk-Change Notification Alerts | Triggers an automated notification when a student's risk status transitions between assessment cycles (e.g., Low -> High). |

---

## 3. Non-Functional Requirements (NFR1 – NFR7)

- **NFR1 - Security**: Passwords salted and hashed with Werkzeug security (`pbkdf2:sha256`); session cookies protected; SQL injection prevented via parameterized queries / SQLAlchemy ORM.
- **NFR2 - Privacy & Data Protection**: Student personal records are isolated by user ID; unauthorized horizontal or vertical privilege escalation is prevented at the controller level.
- **NFR3 - Usability**: Clean, responsive web design using Bootstrap 5 and Chart.js. Zero technical barrier for faculty or students.
- **NFR4 - Performance**: ML inference latency under 50ms per record; dashboard page load under 500ms; lightweight local SQLite database.
- **NFR5 - Reliability & Data Integrity**: Foreign key constraints, unique constraints, and ACID transactions ensure consistency across records and prediction logs.
- **NFR6 - Maintainability & Modularity**: 5-layer modular architecture separating presentation, routing, business services, data access, and model persistence.
- **NFR7 - Portability & Zero-Config Execution**: Operates out-of-the-box on standard Windows 10/11 laptops without requiring Docker, cloud services, or paid external APIs.

---

## 4. Technology Stack Justification

| Component | Selected Technology | Justification |
|---|---|---|
| **Programming Language** | **Python 3.11** | Standard language for AI/ML and rapid web development in academic curriculum. |
| **Web Framework** | **Flask 3.x** | Lightweight, pythonic, modular, ideal for educational lab projects without the heavy boilerplate of Django. |
| **Frontend** | **HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js** | Modern, responsive UI with interactive data visualizations for risk distribution and trends. |
| **Database** | **SQLite 3 (via SQLAlchemy 2.0)** | Zero-configuration, serverless, self-contained single-file relational DB perfectly conforming to Experiment 5 schema. |
| **Machine Learning** | **Scikit-Learn, Pandas, NumPy, Joblib** | Industry-standard libraries for tabular data preprocessing, model training, evaluation, and serialized pipeline persistence. |
| **Testing** | **PyTest 8.x** | Robust automated testing framework for unit tests, model verification, and integration flows. |
| **Version Control & CI** | **Git, GitHub, GitHub Actions** | Standard workflow matching Experiments 9 and 10 requirements. |

---

## 5. Five-Layer System Architecture

As formally designed in **Experiment 4**, the application is structured as a 5-layer modular monolith:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Presentation Layer (UI / Templates / Static Assets)      │
│    - Jinja2 HTML5 Templates, Bootstrap 5, FontAwesome,     │
│    - Chart.js (Interactive Risk & Attendance Charts)       │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS / Form POST / JSON
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Application Layer (Controllers & Authentication)          │
│    - Flask Blueprints: auth, faculty, student, admin, api   │
│    - Session management, RBAC decorators, input validation  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Service Method Invocations
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Business & Machine Learning Layer                        │
│    - AcademicDataService (Record creation, CSV parsing)     │
│    - PredictionService (ML pipeline inference, scoring)     │
│    - ExplainabilityService (Feature contribution calculation)│
│    - NotificationService (Cycle risk-change detection)      │
│    - ReportingService (Aggregations & summary metrics)      │
└──────────────────────────────┬──────────────────────────────┘
                               │ Data Access Calls
┌──────────────────────────────▼──────────────────────────────┐
│ 4. Data Access Layer (Repositories & Adapters)              │
│    - UserRepository, AcademicRepository, PredictionRepo     │
│    - MLModelAdapter (Loads serialized .joblib artifact)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Storage Read / Write
┌──────────────────────────────▼──────────────────────────────┐
│ 5. Storage Layer                                            │
│    - Relational Database: SQLite (student_system.db)        │
│    - ML Model Artifacts: ml/models/best_student_model.joblib│
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Major Application Modules

1. **Authentication & RBAC (`app/routes/auth.py`)**:
   - Handles login, logout, registration (with role enforcement), and session state.
2. **Faculty Portal (`app/routes/faculty.py`)**:
   - Student roster viewing, filterable by risk tier.
   - Single student academic record entry & CSV batch upload.
   - Assessment cycle selection and batch prediction execution.
   - Student detailed academic trajectory view with alerts.
3. **Student Portal (`app/routes/student.py`)**:
   - Confidential self-service dashboard showing personal attendance, internal marks, current risk level, and AI-generated actionable suggestions.
4. **Admin / HOD Dashboard (`app/routes/admin.py`)**:
   - High-level department overview: student count, risk breakdown, faculty allocations, and class performance distributions.
5. **Machine Learning & Prediction Service (`app/services/prediction_service.py` & `ml/`)**:
   - Preprocesses student feature vector: `[attendance_pct, internal_marks, assignment_score, participation_score, prev_sem_marks]`.
   - Generates risk category (`Low`, `Medium`, `High`) and risk score (0.0 to 1.0).
   - Extracts contributing risk factors using model weights / feature contributions.
   - Compares with previous cycle prediction and generates notification if risk worsened or improved.

---

## 7. Database Implementation Plan (Conforming to Exp 5)

The database strictly implements the 14 relational tables designed and normalized to 3NF in Experiment 5:
1. `users`
2. `departments`
3. `classes`
4. `students`
5. `faculty`
6. `subjects`
7. `teaching_assignments`
8. `assessment_cycles`
9. `academic_records`
10. `ml_models`
11. `predictions`
12. `prediction_factors`
13. `suggestions`
14. `notifications`

Primary keys, foreign keys, unique constraints (e.g. `roll_no`, `(student_id, subject_id, cycle_id)`), and cascading deletes for child prediction records will be enforced.

---

## 8. Machine Learning Implementation Plan

1. **Dataset**: Prepare a realistic, reproducible academic dataset (`ml/dataset/student_academic_data.csv`) explicitly labeled as synthetic institutional demonstration data.
2. **Algorithms Evaluated**:
   - Logistic Regression (Baseline linear classifier)
   - Decision Tree Classifier (Interpretable tree splits)
   - Random Forest Classifier (Ensemble method with high accuracy and robustness)
3. **Evaluation Metrics**: Multi-class Accuracy, Precision, Recall, Macro F1-score, and Confusion Matrix.
4. **Model Selection**: Automatically select and persist the best performing model pipeline (including StandardScaler / Preprocessing) to `ml/models/best_student_model.joblib`.
5. **Metadata Logging**: Store model hyperparameters, accuracy, and F1-score in the `ml_models` database table for governance and auditability.
6. **Factor Extraction**: Derive top positive/negative feature impacts for each individual prediction to satisfy FR5.

---

## 9. Project Directory Structure

```
SE Project/
│
├── .github/
│   └── workflows/
│       └── tests.yml                 # Automated CI workflow
│
├── app/                              # Flask application package
│   ├── __init__.py                   # App factory and blueprint registration
│   ├── config.py                     # App configuration (dev, test, prod)
│   ├── models/                       # SQLAlchemy ORM models (14 entities)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── academic.py
│   │   └── prediction.py
│   ├── routes/                       # Web controllers
│   │   ├── __init__.py
│   │   ├── auth.py                   # Login, register, logout
│   │   ├── faculty.py                # Faculty dashboard, entry, prediction
│   │   ├── student.py                # Student self-service portal
│   │   ├── admin.py                  # HOD aggregate analytics
│   │   └── api.py                    # JSON APIs for charts & async checks
│   ├── services/                     # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── academic_service.py
│   │   ├── prediction_service.py     # Inference & factor explainability
│   │   └── notification_service.py   # Risk transition alerts
│   ├── templates/                    # Jinja2 HTML templates
│   │   ├── base.html                 # Navigation bar & layout shell
│   │   ├── auth/                     # Login & register views
│   │   ├── faculty/                  # Faculty dashboard & data entry
│   │   ├── student/                  # Student portal & advice
│   │   └── admin/                    # HOD department analytics
│   └── static/                       # Static CSS, JS, and images
│       ├── css/style.css
│       └── js/charts.js
│
├── database/                         # Database scripts
│   ├── schema.sql                    # Pure DDL script
│   ├── init_db.py                    # Database creation script
│   └── seed_data.py                  # Demonstration dataset seeder
│
├── ml/                               # Machine Learning module
│   ├── dataset/                      # CSV training datasets
│   │   └── student_academic_data.csv
│   ├── models/                       # Serialized model artifacts (.joblib)
│   │   └── best_student_model.joblib
│   ├── preprocessing.py              # Feature cleaning & scaling
│   ├── train_model.py                # Model training & model comparison
│   ├── evaluate_model.py             # Evaluation report & confusion matrix
│   └── predict.py                    # Standalone prediction runner & tester
│
├── tests/                            # Automated test suite (PyTest)
│   ├── conftest.py                   # Test fixtures & temporary test DB
│   ├── unit/                         # Unit tests
│   │   ├── test_auth.py
│   │   ├── test_models.py
│   │   ├── test_preprocessing.py
│   │   └── test_prediction_service.py
│   └── integration/                  # End-to-end integration tests
│       ├── test_faculty_workflow.py
│       ├── test_student_workflow.py
│       └── test_api_routes.py
│
├── docs/                             # Complete project documentation
│   ├── reference/                    # Preserved reference materials
│   │   ├── EXPERIMENT_LIST.md
│   │   ├── OUR_PROJECT_DOCUMENTATION.md
│   │   └── TEACHER_REFERENCE_GUIDE.md
│   ├── DEVELOPMENT_PLAN.md           # This master document
│   ├── REQUIREMENTS_TRACEABILITY.md  # SRS to code & test mapping
│   ├── PROGRESS.md                   # Real-time milestone tracker
│   ├── TEAM_COLLABORATION.md         # 4-member task allocation & Git rules
│   ├── TEST_PLAN.md                  # Test strategy & test cases
│   ├── TEST_REPORT.md                # Actual execution test results
│   ├── SCREENSHOTS_CHECKLIST.md      # Lab manual screenshot instructions
│   ├── USER_MANUAL.md                # User operational handbook
│   ├── TECHNICAL_DOCUMENTATION.md    # System architecture & API specs
│   ├── GITHUB_GUIDE.md               # Git branching & PR guide
│   ├── RETROSPECTIVE.md              # Post-project review & learnings
│   └── VIVA_PREPARATION.md           # Final viva voce Q&A guide
│
├── .env.example                      # Sample environment variables
├── .gitignore                        # Python & IDE ignore rules
├── requirements.txt                  # Python dependencies
├── README.md                         # Project setup & execution guide
└── run.py                            # Application entry point
```

---

## 10. Testing Strategy

The testing strategy is aligned with **Experiment 8** (Unit and Integration testing) and **Experiment 11** (Test Plan and Execution):
- **Framework**: `pytest` and `pytest-flask`.
- **Unit Testing**:
  - `test_auth.py`: Password hashing, session storage, invalid credentials, unauthorized role access.
  - `test_models.py`: Database model creation, foreign key relationships, validation constraints.
  - `test_preprocessing.py`: Handling outliers, scaling, missing data interpolation.
  - `test_prediction_service.py`: Inference pipeline, risk categorization logic, factor breakdown calculation.
- **Integration Testing**:
  - `test_faculty_workflow.py`: End-to-end flow of logging in as faculty, uploading academic records, triggering ML prediction, and verifying updated predictions in the database.
  - `test_student_workflow.py`: End-to-end verification that a student can only view their own records and see early warning alerts.
  - `test_api_routes.py`: API responses for dashboard charts and AJAX filtering.

---

## 11. Git, Collaboration, and CI Strategy

- **Branching Model** (Experiment 9):
  - `main`: Production-ready, stable codebase.
  - `develop`: Integration branch where tested feature branches merge.
  - `feature/<module-name>`: Individual work branches (e.g., `feature/ml-pipeline`, `feature/faculty-portal`, `feature/auth-service`).
- **Pull Request Protocol**:
  - Every PR must pass automated CI tests before merging.
  - Peer review checklist: code formatting, no hardcoded credentials, test coverage included.
- **Continuous Integration** (Experiment 10):
  - GitHub Actions workflow running on Ubuntu and Windows.
  - Steps: Checkout repo -> Set up Python 3.11 -> Install dependencies -> Train/verify ML artifact -> Run pytest suite -> Report execution summary.

---

## 12. Four-Member Task Distribution

| Team Member | Role Title | Primary Modules & Responsibilities | Deliverables Owned |
|---|---|---|---|
| **Member 1** | Frontend & Visualization Lead | UI/UX Design, Jinja2 Templates, Bootstrap 5 styling, Chart.js implementation, Faculty/Student responsive views. | Frontend templates, Static CSS/JS, UI Screenshots for Lab Record. |
| **Member 2** | Backend & Authentication Lead | Flask Application Factory, Route Controllers, Authentication & Session RBAC, API endpoints, Input validation. | `app/routes/`, `app/auth/`, Session handling, API controllers. |
| **Member 3** | AI/ML & Prediction Lead | Dataset synthesis & validation, Model training (Random Forest, Decision Tree, Logistic Regression), Pipeline export, Feature factor explainability, Suggestion generation. | `ml/` folder, `.joblib` model pipeline, ML evaluation reports, Feature importance logic. |
| **Member 4** | Database, QA & DevOps Lead | Relational schema creation (3NF), Seed data generation, PyTest unit & integration tests, GitHub Actions CI workflow, Documentation & Viva guide. | `database/`, `tests/`, `.github/workflows/`, Lab manual documentation & Viva Q&A. |

---

## 13. Development Milestones

1. **Milestone 1**: Requirements verification & Development Plan finalization (Current).
2. **Milestone 2**: Database schema implementation and seeding with realistic student cohorts.
3. **Milestone 3**: ML model dataset curation, model comparison, training, and artifact persistence.
4. **Milestone 4**: Core backend application, authentication, and RBAC service integration.
5. **Milestone 5**: Role-based web dashboards (Faculty, Student, HOD) with dynamic Chart.js visualizations.
6. **Milestone 6**: Early warning triggers, factor explainability, and risk transition notifications.
7. **Milestone 7**: Automated test suite execution (Unit & Integration tests via PyTest).
8. **Milestone 8**: Git workflow setup and GitHub Actions CI pipeline configuration.
9. **Milestone 9**: Complete technical documentation, user guide, test reports, and viva preparation.
10. **Milestone 10**: End-to-end local execution verification on Windows and clean demonstration walkthrough.
