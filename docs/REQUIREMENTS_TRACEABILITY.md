# Requirements Traceability Matrix (RTM)
## AI-Based Student Performance Prediction and Early Warning System
**Course**: B.Tech CSE (AIML) 5th Semester | **Lab**: Software Engineering Lab (JCSAIMLL-001)

This matrix maps each requirement from the Software Requirements Specification (Experiment 2) to its design artifact, implementing source code files, database entities, and verifying automated test cases.

---

### Functional Requirements Traceability

| Req ID | Requirement Description | UML Design Artifact | Implementing Module / Source Files | Database Tables Involved | Verifying Test Cases |
|---|---|---|---|---|---|
| **FR1** | Secure registration & login for students, faculty, and admins | Use Case: `Register`, `Log in`; Class: `User` | `app/routes/auth.py`<br>`app/services/auth_service.py`<br>`app/models/user.py` | `users` | `tests/unit/test_auth.py::test_user_registration`<br>`tests/unit/test_auth.py::test_user_login_success`<br>`tests/unit/test_auth.py::test_user_invalid_password` |
| **FR2** | Academic data entry & bulk CSV upload by faculty | Use Case: `Enter / upload academic data`; Class: `AcademicRecord` | `app/routes/faculty.py`<br>`app/services/academic_service.py` | `academic_records`<br>`students`<br>`subjects`<br>`assessment_cycles` | `tests/integration/test_faculty_workflow.py::test_academic_record_entry`<br>`tests/integration/test_faculty_workflow.py::test_csv_bulk_upload` |
| **FR3** | Data preprocessing & cleaning before use | Included Use Case: `Validate and preprocess data` | `ml/preprocessing.py`<br>`app/services/prediction_service.py` | `academic_records` | `tests/unit/test_preprocessing.py::test_clean_and_scale_features`<br>`tests/unit/test_preprocessing.py::test_handle_missing_values` |
| **FR4** | ML-based prediction of risk category (`Low`, `Medium`, `High`) & score | Class: `MLModel`, `Prediction`; Service: `PredictionService` | `ml/predict.py`<br>`ml/train_model.py`<br>`app/services/prediction_service.py` | `ml_models`<br>`predictions` | `tests/unit/test_prediction_service.py::test_prediction_classification`<br>`tests/unit/test_prediction_service.py::test_model_artifact_loading` |
| **FR5** | Display key contributing factors for each prediction | Class: `PredictionFactor`; Use Case: `Identify contributing factors` | `app/services/prediction_service.py`<br>`app/templates/faculty/student_detail.html` | `prediction_factors` | `tests/unit/test_prediction_service.py::test_contributing_factors_generation` |
| **FR6** | Faculty dashboard filterable by risk category | Use Case: `View assigned students and filter by risk` | `app/routes/faculty.py`<br>`app/templates/faculty/dashboard.html` | `students`<br>`predictions`<br>`teaching_assignments` | `tests/integration/test_faculty_workflow.py::test_filter_students_by_risk` |
| **FR7** | Student dashboard with personal risk status & improvement suggestions | Use Case: `View own performance and risk status`, `View suggestions` | `app/routes/student.py`<br>`app/templates/student/dashboard.html` | `predictions`<br>`suggestions`<br>`academic_records` | `tests/integration/test_student_workflow.py::test_student_dashboard_access`<br>`tests/integration/test_student_workflow.py::test_student_suggestions_display` |
| **FR8** | Admin / HOD dashboard showing department/class aggregates | Use Case: `View department / class aggregates` | `app/routes/admin.py`<br>`app/templates/admin/dashboard.html` | `departments`<br>`classes`<br>`students`<br>`predictions` | `tests/integration/test_api_routes.py::test_admin_aggregate_statistics` |
| **FR9** | Role-based data access control (student: own data; faculty: assigned classes; HOD: aggregates) | Sequence Diagram Lifelines & Access Checks | `app/services/auth_service.py` (decorators `@login_required`, `@role_required`) | `teaching_assignments`<br>`students`<br>`users` | `tests/integration/test_student_workflow.py::test_student_cannot_access_other_student_data`<br>`tests/unit/test_auth.py::test_unauthorized_role_access` |
| **FR10** | Prediction updates across assessment cycles (IA-1, IA-2, etc.) | Class: `AssessmentCycle`; Activity Diagram cycle branch | `app/routes/faculty.py`<br>`app/services/prediction_service.py` | `assessment_cycles`<br>`predictions` | `tests/integration/test_faculty_workflow.py::test_multi_cycle_predictions` |
| **FR11** | Basic performance reporting and summaries | Use Case: `Generate performance reports` | `app/routes/faculty.py`<br>`app/routes/admin.py`<br>`app/templates/reports/` | `predictions`<br>`academic_records`<br>`classes` | `tests/integration/test_api_routes.py::test_generate_performance_report` |
| **Elicited** | Notification / alert on risk category change | UML Extension: `Notify on risk-level change`; Class: `Notification` | `app/services/notification_service.py`<br>`app/models/prediction.py` | `notifications` | `tests/unit/test_prediction_service.py::test_risk_transition_notification` |

---

### Non-Functional Requirements Traceability

| Req ID | Quality Attribute | Architectural / Technical Mechanism | Verifying Test Case / Method |
|---|---|---|---|
| **NFR1** | Security | Password hashing via `werkzeug.security` (PBKDF2-HMAC-SHA256), session cookie protection, CSRF mitigation | `tests/unit/test_auth.py::test_password_hashing_security` |
| **NFR2** | Privacy | Row-level data isolation via session-bound queries; prevention of IDOR (Insecure Direct Object References) | `tests/integration/test_student_workflow.py::test_privacy_isolation` |
| **NFR3** | Usability | Responsive Bootstrap 5 UI, intuitive color-coded risk badges (Green/Yellow/Red), interactive Chart.js graphs | Verified via UI navigation tests & browser inspection |
| **NFR4** | Performance | In-memory cached model pipeline, sub-50ms inference latency, indexed foreign key lookups | `tests/unit/test_prediction_service.py::test_prediction_latency` |
| **NFR5** | Reliability | SQLite ACID compliance, foreign key integrity, schema unique constraints, automated rollback on failure | `tests/unit/test_models.py::test_database_integrity_constraints` |
| **NFR6** | Maintainability | Strict 5-layer modular architecture; interchangeable ML model adapter without modifying web UI | `tests/unit/test_prediction_service.py::test_modular_model_adapter` |
| **NFR7** | Scalability & Portability | Standalone Python packaging, relative path imports, cross-platform Windows/Linux execution | Verified via GitHub Actions CI matrix and clean virtualenv tests |
