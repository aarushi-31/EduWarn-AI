# JSS UNIVERSITY, NOIDA
## Department of Computer Science and Engineering (AIML)
### Software Engineering Lab (JCSAIMLL-001) - 5th Semester B.Tech
### Project: AI-Based Student Performance Prediction and Early Warning System

---

## EXPERIMENT 1: Problem Selection, Feasibility Study, and Project Charter

### 1. Technical Feasibility Study
The proposed project analyzes student academic data (attendance, internal assessment marks, assignment scores, previous examination performance, and participation) to predict the likelihood of poor academic performance in upcoming examinations.
- **Technologies**: Python, Flask / FastAPI, Scikit-learn, Pandas, NumPy, MySQL / PostgreSQL (or SQLite for zero-config portable deployment), HTML/CSS/JavaScript/Bootstrap, Chart.js.
- **Hardware**: Standard computer/laptop with basic specs.

### 2. Economic Feasibility Study
- Software and libraries: Free and open-source (₹0).
- Development hardware: Existing student/college systems (₹0).
- Database & ML tools: Open-source (₹0).
- Total estimated additional cost: Minimal/Zero.

### 3. Operational Feasibility Study
- Supports existing academic workflows as a decision-support tool.
- Faculty members retain authority and judgment; the system does not make automated disciplinary or grading verdicts.
- Simple, user-friendly interface accessible on any desktop or mobile browser.

### 4. Schedule Feasibility Study
- 10-week development plan across requirements, design, dataset prep, model training, backend, frontend, integration, testing, and final documentation.

### 5. Project Charter Summary
- **Title**: AI-Based Student Performance Prediction and Early Warning System.
- **Objectives**: Collect academic data, train classification ML models, predict risk categories (Low, Medium, High), highlight key contributing factors, deliver actionable improvement suggestions, alert on risk changes, and provide role-based dashboards.
- **Stakeholders**: Students, Faculty Members, Department Head (HOD), College Administration, Project Team, Project Guide.
- **Target Users**:
  1. Faculty Members: Monitor assigned students, view predictions and contributing factors, trigger predictions.
  2. Students: View personal academic history, predicted risk category, improvement recommendations, and alerts.
  3. Administrators / HOD: Monitor department-level aggregated statistics and risk distributions.

---

## EXPERIMENT 2: Requirements Elicitation and SRS

### Functional Requirements (FR1 - FR11)
- **FR1**: System shall allow students and faculty to register and log in securely.
- **FR2**: System shall allow faculty to enter or upload student academic data (attendance, internal marks, assignment scores, previous performance, participation).
- **FR3**: System shall preprocess and clean uploaded data before use.
- **FR4**: System shall use a trained ML model to predict a risk category (`Low`, `Medium`, `High`) for each student.
- **FR5**: System shall display, for each prediction, the key contributing factors (explainability).
- **FR6**: System shall provide a faculty dashboard listing students filterable by risk category.
- **FR7**: System shall provide a student dashboard showing the student's own risk status and improvement suggestions.
- **FR8**: System shall provide an admin/HOD dashboard showing department/class-level aggregated statistics.
- **FR9**: System shall restrict data visibility based on user role (faculty: assigned students only; HOD: aggregated data; student: own data only).
- **FR10**: System shall update predictions after each internal assessment cycle.
- **FR11**: System shall generate basic performance reports.
- **Stakeholder Elicitation Requirement**: Alert/notify user when a student's risk category changes from a previous assessment cycle.

### Non-Functional Requirements (NFR1 - NFR7)
- **NFR1 - Security**: Authentication and role-based access control (RBAC), password hashing (bcrypt/werkzeug).
- **NFR2 - Privacy**: Student data is confidential and visible only to the student and authorized faculty/administrators.
- **NFR3 - Usability**: Clean, responsive, intuitive UI with Bootstrap 5 and Chart.js.
- **NFR4 - Performance**: Fast model inference (<100ms) and low latency database queries.
- **NFR5 - Reliability**: ACID transactions, schema integrity, data validation.
- **NFR6 - Maintainability**: Modular 5-layer architecture; decouple ML model artifact from application logic.
- **NFR7 - Scalability**: Modular design supporting additional classes, students, and assessment cycles.

---

## EXPERIMENT 3: UML Diagrams

1. **Use Case Diagram**:
   - Actors: Student, Faculty, Administrator / HOD.
   - Use Cases: Register, Log In, View Own Performance & Risk Status, View Improvement Suggestions, Enter/Upload Academic Data, Generate Predictions, Validate & Preprocess Data (`<<include>>`), Identify Contributing Factors (`<<include>>`), View Assigned Students & Filter by Risk, Generate Performance Reports, View Department/Class Aggregates, Notify on Risk-Level Change (`<<extend>>`).

2. **Class Diagram**:
   - Core Classes: `User`, `Student`, `Faculty`, `AdministratorHOD`, `Department`, `AcademicClass`, `Subject`, `TeachingAssignment`, `AssessmentCycle`, `AcademicRecord`, `MLModel`, `Prediction`, `PredictionFactor`, `Suggestion`, `Notification`, `PredictionService`.

3. **Activity Diagram**:
   - Workflow: Faculty login -> Verify credentials -> Select Assessment Cycle & Subject -> Enter or upload academic records -> Validation checks -> Data cleaning & feature extraction -> ML Model prediction -> Extract contributing factors & suggestions -> Check for risk category transition -> Generate notifications if changed -> Display results to faculty.

4. **Sequence Diagram**:
   - Actors and Lifelines: Faculty / Student -> Web Interface -> Application Controller -> Authentication Handler -> Prediction Service -> ML Model Adapter -> Database / Repository.

---

## EXPERIMENT 4: Architectural Design (5-Layer Modular Monolith)

1. **Layer 1: Presentation Layer**: Web interface (HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js).
2. **Layer 2: Application Layer**: Flask controllers, session-based auth, role-based decorators, input validation.
3. **Layer 3: Business & ML Layer**: Academic data service, ML prediction pipeline, factor explainability engine, suggestion rules, notification triggers, aggregation service.
4. **Layer 4: Data Access Layer**: Repository classes executing parameterized queries / SQLAlchemy ORM mappings, ML model loader.
5. **Layer 5: Storage Layer**: Relational Database (SQLite/MySQL/PostgreSQL) and versioned Scikit-learn model artifact files (`.joblib` / `.pkl`).

---

## EXPERIMENT 5: Database Design and Relational Schema

### 14 Normalized Entities (3NF)
1. `USER(user_id PK, username, password_hash, email, role, created_at)`
2. `DEPARTMENT(dept_id PK, dept_name, hod_id FK -> FACULTY)`
3. `CLASS(class_id PK, dept_id FK -> DEPARTMENT, section, semester, academic_year)`
4. `STUDENT(student_id PK, user_id FK -> USER, class_id FK -> CLASS, roll_no, name)`
5. `FACULTY(faculty_id PK, user_id FK -> USER, dept_id FK -> DEPARTMENT, name)`
6. `SUBJECT(subject_id PK, dept_id FK -> DEPARTMENT, subject_code, subject_name)`
7. `TEACHING_ASSIGNMENT(assignment_id PK, faculty_id FK, subject_id FK, class_id FK)`
8. `ASSESSMENT_CYCLE(cycle_id PK, cycle_name, start_date, end_date)`
9. `ACADEMIC_RECORD(record_id PK, student_id FK, subject_id FK, cycle_id FK, entered_by FK -> FACULTY, attendance_pct, internal_marks, assignment_score, participation_score, prev_sem_marks)`
10. `ML_MODEL(model_id PK, algorithm, version, accuracy, f1_score, trained_on)`
11. `PREDICTION(prediction_id PK, student_id FK, cycle_id FK, model_id FK, risk_category, risk_score, predicted_at)`
12. `PREDICTION_FACTOR(factor_id PK, prediction_id FK, feature_name, contribution)`
13. `SUGGESTION(suggestion_id PK, prediction_id FK, suggestion_text)`
14. `NOTIFICATION(notification_id PK, user_id FK, prediction_id FK, message, is_read, created_at)`
