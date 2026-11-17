# AI-Based Student Performance Prediction and Early Warning System
**Software Engineering Laboratory Project (JCSAIMLL-001)**  
**Department of Computer Science & Engineering (AIML)**  
**JSS University, Noida**  
**Academic Year**: 2026–2027 | **Semester**: 5th Semester B.Tech

---

## Abstract

Higher educational institutions face critical challenges in identifying struggling students early enough to intervene effectively. Traditional evaluation methods review marks only after examinations conclude, often too late to prevent course failure or attendance-based detention.

The **AI-Based Student Performance Prediction and Early Warning System (EduWarn AI)** is an explainable decision-support platform engineered to solve this problem. Developed as our 5th-semester Software Engineering Lab capstone, the system analyzes continuous academic indicators—attendance percentage, internal assessment marks, assignment scores, classroom participation, and prior semester performance—using supervised machine learning. 

The application classifies student academic risk into **Low Risk**, **Medium Risk**, and **High Risk**, extracts key diagnostic contributing factors (Explainable AI), delivers personalized improvement suggestions, and dispatches automated early-warning alerts when a student's risk category escalates across assessment cycles.

The project strictly implements all 13 prescribed laboratory experiments, conforms to our Experiment 1–5 SRS, UML, 5-layer architecture, and 3NF database design, and is 100% verified via a 29-test PyTest automated suite and GitHub Actions CI.

---

## Key Features

- **Decision Support, Not Decision Replacement**: Supports faculty judgment with transparent, explainable recommendations without automating final grading or punitive verdicts.
- **5-Layer Modular Architecture**: Presentation, Application (Flask Blueprints), Business & ML Services, Data Access, and Storage (SQLite).
- **14-Table Relational Schema in 3NF**: Fully normalized relational schema with primary/foreign keys, unique constraints, and cascade delete rules.
- **Multi-Model Machine Learning Pipeline**: Scikit-Learn pipeline comparing Logistic Regression, Decision Tree, and Random Forest; champion model achieves **87.08% accuracy** and **86.00% macro F1-score**.
- **Factor Explainability (FR5)**: Translates model feature weights into natural-language diagnostic observations (e.g. "Attendance is severely low at 52.0%").
- **Actionable Guidance Engine (FR7)**: Provides students with clear remedial recommendations (e.g. "Attend next 14 lectures without absence").
- **Early Warning Risk Transition Alerts**: Automatically detects when a student shifts between risk tiers across internal assessment cycles (IA-1, IA-2) and alerts both student and teacher.
- **Role-Based Portals & Privacy**:
  - **Faculty Portal**: Student roster, risk filters, manual marks entry, and batch CSV upload.
  - **Student Portal**: Confidential self-service view of personal scores, risk badge, and notifications.
  - **HOD / Admin Portal**: Department aggregate metrics, Chart.js doughnut chart, class health breakdowns, and printable PDF reports.

---

## Laboratory Experiments Alignment (1 to 13)

| Exp # | Experiment Title | Implementation Artifacts in Workspace |
|---|---|---|
| **1** | Problem Selection, Feasibility Study & Project Charter | `docs/reference/OUR_PROJECT_DOCUMENTATION.md` |
| **2** | Requirements Elicitation & SRS (FR1–FR11, NFR1–NFR7) | `docs/DEVELOPMENT_PLAN.md`, `docs/REQUIREMENTS_TRACEABILITY.md` |
| **3** | UML Diagrams (Use Case, Class, Activity, Sequence) | Preserved in reference documentation and implemented in `app/models/` |
| **4** | Layered Architectural Design (5-Layer Monolith) | `app/` (presentation, routes, services, data access, storage) |
| **5** | Database Design (ER Diagram & 14-Table 3NF Schema) | `database/schema.sql`, `app/models/`, `database/init_db.py` |
| **6** | Implementation of Core Application Modules | `app/routes/`, `app/services/`, `app/templates/` |
| **7** | Module Integration & Early Warning System | Integrated ML pipeline with database triggers and notifications |
| **8** | Automated Unit and Integration Testing | `tests/unit/`, `tests/integration/` (29 automated tests via PyTest) |
| **9** | Git Version Control & Branching Workflow | `docs/GITHUB_GUIDE.md`, `docs/TEAM_COLLABORATION.md`, `.gitignore` |
| **10** | Continuous Integration (CI) Workflow | `.github/workflows/tests.yml` (multi-OS automated build & test) |
| **11** | Test Plan and Actual Test Execution Report | `docs/TEST_PLAN.md`, `docs/TEST_REPORT.md` (100% pass rate) |
| **12** | Documentation, Retrospective & Manual | `docs/USER_MANUAL.md`, `docs/TECHNICAL_DOCUMENTATION.md`, `docs/RETROSPECTIVE.md` |
| **13** | Final Demonstration & Viva Voce Preparation | `docs/VIVA_PREPARATION.md`, `docs/SCREENSHOTS_CHECKLIST.md` |

---

## Quick Demo Credentials

For laboratory practical examinations and grading evaluations, convenient demo buttons are provided on the login page, or use these credentials:

| Role | Name | Username | Password | Key Capabilities |
|---|---|---|---|---|
| **Faculty Member** | Prof. Neha Gupta | `faculty_neha` | `FacultyPassword123!` | Monitor roster, filter by risk, enter marks, upload CSV |
| **Student (High Risk)** | Rohit Sharma | `student_rohit` | `StudentPassword123!` | View personal High Risk standing, explainability, alerts |
| **Student (Low Risk)** | Aarav Patel | `student_aarav` | `StudentPassword123!` | View on-track standing, positive factors, advanced advice |
| **Department Head (HOD)** | Dr. Ramesh Sharma | `admin_hod` | `AdminPassword123!` | Department overview, Chart.js pie chart, official reports |

---

## Local Setup & Execution Guide (Windows 10 / 11)

### 1. Prerequisites
- **Python 3.11.x** installed (ensure "Add Python to PATH" is checked during install).
- **Git** installed.

### 2. Clone the Repository
```powershell
git clone https://github.com/your-team/student-performance-prediction.git
cd "student-performance-prediction"
```

### 3. Create and Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Initialize Database & Seed Demonstration Cohort
```powershell
python database/seed_data.py
python database/init_db.py --status
```
*Creates all 14 relational tables in `instance/student_performance.db` and seeds 20 student accounts, faculty, and academic records.*

### 6. Train & Evaluate Machine Learning Models
```powershell
python ml/dataset/generate_dataset.py
python ml/train_model.py
python ml/evaluate_model.py
```
*Compares Logistic Regression, Decision Tree, and Random Forest; saves champion pipeline to `ml/models/best_student_model.joblib` and generates `ml/models/confusion_matrix.png`.*

### 7. Populate Initial Predictions
```powershell
python database/populate_initial_predictions.py
```
*Generates baseline predictions, explainability factors, and suggestions for IA-1 and IA-2.*

### 8. Run Automated Test Suite (PyTest)
```powershell
pytest -v
```
*Runs all 29 unit and integration tests (100% pass rate).*

### 9. Start the Web Server
```powershell
python run.py
```
*Launches the server at `http://127.0.0.1:5000/`.*

### 10. Access in Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## Project Directory Layout

```
SE Project/
│
├── .github/
│   └── workflows/
│       └── tests.yml                 # GitHub Actions automated CI pipeline
│
├── app/                              # Flask Application Package
│   ├── __init__.py                   # Application Factory & Blueprint registry
│   ├── db.py                         # SQLAlchemy scoped session & database engine
│   ├── models/                       # 14 Relational Models (3NF)
│   │   ├── __init__.py
│   │   ├── user.py                   # User, Department, Class, Faculty, Student
│   │   ├── academic.py               # Subject, TeachingAssignment, Cycle, AcademicRecord
│   │   └── prediction.py             # MLModel, Prediction, Factor, Suggestion, Notification
│   ├── routes/                       # Web Controllers
│   │   ├── __init__.py
│   │   ├── auth.py                   # Login, register, logout handlers
│   │   ├── faculty.py                # Faculty roster, filters, entry, CSV upload
│   │   ├── student.py                # Student self-service & alerts
│   │   ├── admin.py                  # HOD department overview & reports
│   │   └── api.py                    # JSON endpoints for Chart.js
│   ├── services/                     # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── auth_service.py           # Session RBAC & decorators
│   │   ├── academic_service.py       # Record CRUD & CSV ingestion
│   │   ├── prediction_service.py     # ML inference & risk transition alerts
│   │   └── notification_service.py   # Alert notification storage
│   ├── templates/                    # Jinja2 HTML5 Templates
│   │   ├── base.html                 # Shell layout, navbar, alert banner
│   │   ├── auth/                     # login.html, register.html
│   │   ├── faculty/                  # dashboard.html, student_detail.html, enter_record.html, upload_csv.html
│   │   ├── student/                  # dashboard.html, notifications.html
│   │   └── admin/                    # dashboard.html, reports.html
│   └── static/                       # Static Assets
│       ├── css/style.css             # Academic theme styling & badges
│       └── js/charts.js              # Chart.js integration scripts
│
├── database/                         # Database Management Scripts
│   ├── schema.sql                    # Pure DDL script (14 tables)
│   ├── init_db.py                    # Table creator & status inspector
│   ├── seed_data.py                  # Demo cohort seeder
│   └── populate_initial_predictions.py# Pre-populates predictions for demo
│
├── ml/                               # Machine Learning Engineering Package
│   ├── dataset/                      # Dataset generator & CSV data
│   │   ├── generate_dataset.py       # Reproducible synthetic dataset script
│   │   └── student_academic_data.csv # 1,200 sample student records
│   ├── models/                       # Serialized models & plots
│   │   ├── best_student_model.joblib # Serialized champion pipeline
│   │   └── confusion_matrix.png      # Saved evaluation confusion matrix
│   ├── preprocessing.py              # Feature validation & StandardScaler
│   ├── train_model.py                # 3-model comparison & training script
│   ├── evaluate_model.py             # Classification report & matrix generator
│   └── predict.py                    # Standalone inference & factor engine
│
├── tests/                            # Automated PyTest Suite
│   ├── conftest.py                   # Test fixtures & test DB setup
│   ├── unit/                         # 17 Unit Tests
│   │   ├── test_auth.py              # Password hashing & authentication
│   │   ├── test_models.py            # Relational models & constraints
│   │   ├── test_preprocessing.py     # Bounds checking & imputation
│   │   └── test_prediction_service.py# Classification, factors & latency
│   └── integration/                  # 12 Integration Tests
│       ├── test_faculty_workflow.py  # Dashboard, filters, entry, CSV upload
│       ├── test_student_workflow.py  # Personal portal & privacy isolation
│       └── test_api_routes.py        # Chart endpoints & HOD reports
│
├── docs/                             # Complete Academic Documentation
│   ├── reference/                    # Preserved Reference Files
│   │   ├── EXPERIMENT_LIST.md        # List of 13 SDLC experiments
│   │   ├── OUR_PROJECT_DOCUMENTATION.md# Preserved Experiments 1 to 5
│   │   └── TEACHER_REFERENCE_GUIDE.md# Academic formatting guidelines
│   ├── DEVELOPMENT_PLAN.md           # Master software development plan
│   ├── REQUIREMENTS_TRACEABILITY.md  # SRS to Code & Test mapping (RTM)
│   ├── PROGRESS.md                   # Milestone execution journal
│   ├── TEAM_COLLABORATION.md         # 4-member task allocation & Git rules
│   ├── TEST_PLAN.md                  # Comprehensive test plan
│   ├── TEST_REPORT.md                # Actual execution test report (29 passed)
│   ├── SCREENSHOTS_CHECKLIST.md      # Lab record evidence capture checklist
│   ├── USER_MANUAL.md                # End-user operational handbook
│   ├── TECHNICAL_DOCUMENTATION.md    # Architecture & mathematical formulations
│   ├── GITHUB_GUIDE.md               # Git branching & PR workflow guide
│   ├── RETROSPECTIVE.md              # Project retrospective (6 questions)
│   └── VIVA_PREPARATION.md           # 20+ common viva questions & demonstration guide
│
├── .env.example                      # Sample local environment variables
├── .gitignore                        # Git ignore patterns
├── requirements.txt                  # Python dependencies
├── run.py                            # Application entry point
└── README.md                         # This master document
```

---

## Team Contributions (4-Member Division)

- **Member 1 (Frontend & UX Lead)**: Designed Jinja2 templates, Bootstrap 5 responsiveness, Chart.js integrations, and user experience for Faculty and Student dashboards.
- **Member 2 (Backend & Security Lead)**: Built Flask application factory, route controllers, PBKDF2 password security, session handling, and role-based access decorators.
- **Member 3 (AI/ML & Explainability Lead)**: Curated the synthetic academic dataset, implemented multi-model training/comparison, feature importance extraction (FR5), and recommendation engine (FR7).
- **Member 4 (Database, QA & DevOps Lead)**: Designed 14-table 3NF schema, seeder scripts, PyTest automated suite (29 tests), GitHub Actions CI pipeline, and comprehensive lab documentation.

---

## License & Academic Disclaimer
Developed solely for academic evaluation in the **Software Engineering Laboratory (JCSAIMLL-001)**, Department of CSE (AIML), JSS University, Noida. Synthetic demonstration records are generated for academic modeling and do not represent actual institutional student data.
