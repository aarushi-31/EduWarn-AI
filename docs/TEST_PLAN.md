# Test Plan
## AI-Based Student Performance Prediction and Early Warning System
**Department of CSE (AIML), JSS University, Noida**  
**Course**: B.Tech 5th Sem | **Lab**: Software Engineering Lab (JCSAIMLL-001)  
**Experiment Reference**: Experiment 11

---

## 1. Testing Objectives
The objective of this test plan is to define the testing strategy, scope, environment, and verification criteria for the AI-Based Student Performance Prediction and Early Warning System. Testing ensures:
- Verification of all 11 Functional Requirements (FR1 to FR11) and elicited stakeholder needs.
- Validation of Non-Functional Requirements (NFR1 - Security, NFR2 - Privacy, NFR3 - Usability, NFR4 - Performance, NFR5 - Reliability, NFR6 - Maintainability).
- Assurance that machine learning inference, factor explainability, and risk transition detection operate accurately and without runtime crashes.

---

## 2. Scope of Testing

### 2.1 In Scope
- **Authentication & RBAC**: User registration, password encryption (PBKDF2/SHA256), login sessions, logout, and role access restrictions for Student, Faculty, and Admin.
- **Academic Data Management**: Single student mark entry, range validations, missing data handling, and bulk CSV ingestion.
- **Machine Learning Inference**: Preprocessing pipeline, model inference, probability calibration, risk scoring, explainability factors, and actionable suggestions.
- **User Interface & Dashboards**: Faculty dashboard risk filtering, student self-service portal, HOD aggregate views, and notification bell counter.
- **Internal APIs & Reporting**: REST/JSON endpoints for Chart.js graphs and printable reports.

### 2.2 Out of Scope
- Load testing exceeding 10,000 concurrent institutional users.
- Automated third-party SMS/WhatsApp gateway deliveries.
- Penetration testing against underlying host operating system kernels.

---

## 3. Testing Approach & Methodology
- **Unit Testing**: Isolated verification of individual functions, modules, algorithms, and data access layers using `pytest`.
- **Integration Testing**: Verification of multi-component interaction flows (e.g., CSV upload triggering ML pipeline, DB persistence, and notification dispatch).
- **Positive Testing**: Verifying system behavior under valid, typical academic inputs (e.g., attendance 85%, marks 24/30).
- **Negative Testing**: Verifying system resilience against boundary, malformed, or malicious inputs (e.g., attendance 120%, negative marks, non-numeric values, unauthorized cross-role route access).

---

## 4. Test Environment

| Component | Specification |
|---|---|
| **Operating System** | Windows 10 / Windows 11 (also tested on Ubuntu Linux via CI) |
| **Python Runtime** | Python 3.11.x |
| **Testing Framework** | PyTest 8.3.x |
| **Database Engine** | SQLite 3 (in-memory and file-based isolated test instance) |
| **Browser Compatibility** | Chrome, Firefox, Edge, Safari |

---

## 5. Master Test Cases Specification

### 5.1 Unit Test Cases (Table 11.1)

| Test ID | Module | Test Condition / Input | Expected Result | Type |
|---|---|---|---|---|
| **UTC-01** | `auth` | Hash password with Werkzeug PBKDF2 | Stored hash is salted and matches input; original plaintext is not stored | Positive |
| **UTC-02** | `auth` | Authenticate with valid username and password | User entity returned with correct role | Positive |
| **UTC-03** | `auth` | Authenticate with wrong password | Returns None; authentication rejected | Negative |
| **UTC-04** | `auth` | Authenticate non-existent username | Returns None; no user found | Negative |
| **UTC-05** | `models` | Verify Student-User 1:1 foreign key linkage | Student profile matches user account and class section | Positive |
| **UTC-06** | `models` | Verify AcademicRecord feature extraction dictionary | Dict contains all 5 required ML feature keys | Positive |
| **UTC-07** | `models` | Verify ML Model metadata query | Model record contains valid accuracy and version | Positive |
| **UTC-08** | `models` | Verify Prediction CSS badge classes | Low -> 'success', Medium -> 'warning', High -> 'danger' | Positive |
| **UTC-09** | `preproc` | Valid academic features within normal bounds | Cleaned dict returned with zero validation errors | Positive |
| **UTC-10** | `preproc` | Missing / None / empty string features | Missing values imputed with academic defaults | Positive |
| **UTC-11** | `preproc` | Features outside legal range (e.g., att=120%, marks=-5) | Errors recorded; values clipped to legal bounds [0, 100] | Negative |
| **UTC-12** | `preproc` | Convert feature dict to 2D numpy matrix | Matrix shape equals (1, 5) with float32 types | Positive |
| **UTC-13** | `ml` | Weak metrics (att=45%, internals=8/30) | Classified as 'High' risk with risk score > 0.65 | Positive |
| **UTC-14** | `ml` | Strong metrics (att=94%, internals=29/30) | Classified as 'Low' risk with risk score < 0.40 | Positive |
| **UTC-15** | `ml` | Factor explainability for attendance < 60% | Flagged as 'Critical' with positive risk contribution | Positive |
| **UTC-16** | `ml` | Inference latency measurement | Mean prediction time under 100 milliseconds | Performance |
| **UTC-17** | `ml` | End-to-end single student prediction service | Prediction, factors, and suggestions saved to DB | Positive |

---

### 5.2 Integration Test Cases (Table 11.2)

| Test ID | Flow | Test Condition / Scenario | Expected Result | Type |
|---|---|---|---|---|
| **ITC-01** | Faculty | Faculty login via `/auth/login` | Session set; redirected to `/faculty/dashboard` | Positive |
| **ITC-02** | Faculty | Filter roster by `risk=High` | Table lists only High risk students | Positive |
| **ITC-03** | Faculty | Filter roster by `risk=Low` | Table lists only Low risk students | Positive |
| **ITC-04** | Faculty | Enter single student record via form | Record saved, ML prediction generated and linked | Positive |
| **ITC-05** | Faculty | Upload valid batch CSV with 2 students | Both records processed, predictions generated | Positive |
| **ITC-06** | Student | Student login via `/auth/login` | Redirected to `/student/dashboard` with personal record | Positive |
| **ITC-07** | Privacy | Student attempts to access `/faculty/dashboard` | Access denied flash message; redirected to student dashboard | Negative |
| **ITC-08** | Student | View notification alerts at `/student/notifications` | Notifications displayed with timestamps | Positive |
| **ITC-09** | Admin | Admin login and access `/admin/dashboard` | Department overview with total student counts displayed | Positive |
| **ITC-10** | Admin | Access printable department report `/admin/reports` | Full academic roster report rendered for printing | Positive |
| **ITC-11** | API | GET `/api/notifications/unread-count` | JSON returned containing unread notification count | Positive |
| **ITC-12** | API | GET `/api/charts/department-risk` | JSON returned with labels ['High', 'Medium', 'Low'] | Positive |

---

## 6. Entry and Exit Criteria
- **Entry Criteria**: Database schema initialized, ML pipeline trained and serialized, web server routes registered.
- **Exit Criteria**: 100% of planned test cases executed; 0 critical or high-severity defects open; all 29 automated PyTest tests passing.
