# Technical Architecture & System Documentation
## AI-Based Student Performance Prediction and Early Warning System
**Department of CSE (AIML), JSS University, Noida**  
**Course**: B.Tech 5th Sem | **Lab**: Software Engineering Lab (JCSAIMLL-001)  
**Experiment Reference**: Experiment 12

---

## 1. System Architecture Overview

The system is engineered as a **5-Layer Modular Monolith**, strictly conforming to the architectural blueprint designed in **Experiment 4**:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Presentation Layer                                       │
│    - Jinja2 HTML5 Templates, Bootstrap 5.3, CSS3, JS       │
│    - Chart.js 4.4 (Doughnut & Bar Visualizations)           │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / Form Data / JSON APIs
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Application Layer (Routing & Access Control)             │
│    - Flask Blueprints: auth, faculty, student, admin, api   │
│    - PBKDF2 Password Security & RBAC Decorators             │
└──────────────────────────────┬──────────────────────────────┘
                               │ Internal Service Invocations
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Business & Machine Learning Layer                        │
│    - PredictionService, AcademicService, NotificationService│
│    - XAI Feature Factor Attribution Engine                  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Scoped SQLAlchemy Sessions
┌──────────────────────────────▼──────────────────────────────┐
│ 4. Data Access Layer                                        │
│    - SQLAlchemy 2.0 ORM Mappings & Scoped Session Factory   │
│    - Serialized ML Pipeline Model Adapter                   │
└──────────────────────────────┬──────────────────────────────┘
                               │ Storage Read / Write
┌──────────────────────────────▼──────────────────────────────┐
│ 5. Storage Layer                                            │
│    - SQLite 3 Relational Database (`student_performance.db`)│
│    - Serialized Scikit-Learn Model (`.joblib` pipeline)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Database Design & Relational Schema (Experiment 5)

The database strictly implements the 14 relational tables normalized to **Third Normal Form (3NF)**:

### 2.1 Table Schemas
1. **`users`**: `(user_id PK, username UNIQUE, password_hash, email UNIQUE, role CHECK('student', 'faculty', 'admin'), created_at)`
2. **`departments`**: `(dept_id PK, dept_name, hod_id FK -> faculty.faculty_id)`
3. **`classes`**: `(class_id PK, dept_id FK -> departments, section, semester CHECK(1-8), academic_year)`
4. **`faculty`**: `(faculty_id PK, user_id FK -> users UNIQUE, dept_id FK -> departments, name)`
5. **`students`**: `(student_id PK, user_id FK -> users UNIQUE, class_id FK -> classes, roll_no UNIQUE, name)`
6. **`subjects`**: `(subject_id PK, dept_id FK -> departments, subject_code UNIQUE, subject_name)`
7. **`teaching_assignments`**: `(assignment_id PK, faculty_id FK, subject_id FK, class_id FK, UNIQUE(faculty_id, subject_id, class_id))`
8. **`assessment_cycles`**: `(cycle_id PK, cycle_name, start_date, end_date)`
9. **`academic_records`**: `(record_id PK, student_id FK, subject_id FK, cycle_id FK, entered_by FK, attendance_pct CHECK(0-100), internal_marks CHECK(>=0), assignment_score CHECK(>=0), participation_score CHECK(>=0), prev_sem_marks CHECK(0-100), UNIQUE(student_id, subject_id, cycle_id))`
10. **`ml_models`**: `(model_id PK, algorithm, version, accuracy, f1_score, trained_on)`
11. **`predictions`**: `(prediction_id PK, student_id FK, cycle_id FK, model_id FK, risk_category CHECK('Low','Medium','High'), risk_score, predicted_at, UNIQUE(student_id, cycle_id, model_id))`
12. **`prediction_factors`**: `(factor_id PK, prediction_id FK ON DELETE CASCADE, feature_name, contribution)`
13. **`suggestions`**: `(suggestion_id PK, prediction_id FK ON DELETE CASCADE, suggestion_text)`
14. **`notifications`**: `(notification_id PK, user_id FK ON DELETE CASCADE, prediction_id FK ON DELETE CASCADE, message, is_read CHECK(0,1), created_at)`

---

## 3. Machine Learning Architecture & Mathematics

### 3.1 Input Feature Space
The machine learning pipeline consumes a 5-dimensional numerical academic vector:
$$\mathbf{x} = [x_1, x_2, x_3, x_4, x_5]^T$$
where:
- $x_1$: Attendance Percentage ($0 \le x_1 \le 100$)
- $x_2$: Internal Examination Marks ($0 \le x_2 \le 30$)
- $x_3$: Assignment Submission Score ($0 \le x_3 \le 25$)
- $x_4$: Classroom Participation Score ($0 \le x_4 \le 20$)
- $x_5$: Previous Semester Marks Percentage ($0 \le x_5 \le 100$)

### 3.2 Preprocessing & Feature Standardization
Features are standardized using Z-score normalization via `StandardScaler`:
$$z_j = \frac{x_j - \mu_j}{\sigma_j}$$
where $\mu_j$ and $\sigma_j$ are the empirical mean and standard deviation estimated on the training split.

### 3.3 Model Comparison & Selection
In `ml/train_model.py`, three algorithms were trained and evaluated using stratified 80/20 train-test splitting on 1,200 samples:
1. **Multinomial Logistic Regression**: 87.08% Accuracy | 86.00% Macro F1
2. **Decision Tree Classifier**: 79.58% Accuracy | 76.40% Macro F1
3. **Random Forest Classifier**: 84.58% Accuracy | 83.24% Macro F1

Multinomial Logistic Regression was selected as the champion model due to highest macro F1-score, zero prediction of High risk as Low risk, and mathematical transparency.

### 3.4 Continuous Risk Score Formulation
The model outputs calibrated posterior class probabilities:
$$P(\text{High} \mid \mathbf{x}), \quad P(\text{Medium} \mid \mathbf{x}), \quad P(\text{Low} \mid \mathbf{x})$$
The scalar risk index $S(\mathbf{x}) \in [0.0, 1.0]$ is computed as:
$$S(\mathbf{x}) = 1.0 \cdot P(\text{High} \mid \mathbf{x}) + 0.5 \cdot P(\text{Medium} \mid \mathbf{x}) + 0.0 \cdot P(\text{Low} \mid \mathbf{x})$$

### 3.5 Explainability & Factor Attribution (FR5)
Feature contributions are extracted by measuring deviations from institutional thresholds (Attendance < 75%, Internals < 18/30) and multiplying by normalized feature coefficients:
$$C_j = w_j \cdot (z_{\text{crit}} - z_j)$$
Top contributors with $C_j > 0.20$ are classified as **Critical** or **Warning** and displayed with natural-language diagnostic text.

---

## 4. Internal API Specifications

| Method | Endpoint | Access Role | Description | Response Format |
|---|---|---|---|---|
| `GET` | `/api/notifications/unread-count` | Authenticated | Fetches unread alert count for navbar badge | `{"unread_count": int}` |
| `GET` | `/api/charts/department-risk` | Admin / Faculty | Fetches risk category counts for Chart.js doughnut | `{"labels": [...], "data": [...], "colors": [...]}` |
| `GET` | `/api/charts/student-metrics/<id>` | Authenticated | Fetches historical cycle metrics for bar chart | `{"cycles": [...], "attendance": [...], ...}` |
