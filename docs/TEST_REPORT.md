# Test Execution Report
## AI-Based Student Performance Prediction and Early Warning System
**Department of CSE (AIML), JSS University, Noida**  
**Course**: B.Tech 5th Sem | **Lab**: Software Engineering Lab (JCSAIMLL-001)  
**Experiment Reference**: Experiment 11

---

## 1. Test Execution Summary

- **Execution Date**: 2026-11-17
- **Test Platform**: Windows 11 / Python 3.11.0 / PyTest 8.3.4
- **Test Runner Command**: `pytest -v`
- **Total Tests Planned**: 29
- **Total Tests Executed**: 29
- **Passed**: 29 (100.0%)
- **Failed**: 0 (0.0%)
- **Execution Duration**: 33.31 seconds
- **Overall Status**: **PASSED (ALL CRITERIA SATISFIED)**

---

## 2. Detailed Test Execution Results (Table 11.3)

| Test Case ID | Test Description | Expected Result | Actual Result | Status | Remarks |
|---|---|---|---|---|---|
| **UTC-01** | Password hashing security with PBKDF2/SHA256 | Plaintext not stored; salted hash verified | Hash starts with `scrypt:`/`pbkdf2:`; verification matches | **PASS** | NFR1 Verified |
| **UTC-02** | User authentication with valid credentials | User entity returned with role | Faculty user entity returned with role='faculty' | **PASS** | FR1 Verified |
| **UTC-03** | User authentication with invalid password | Returns None | Returns None | **PASS** | FR1 Verified |
| **UTC-04** | User authentication with non-existent user | Returns None | Returns None | **PASS** | FR1 Verified |
| **UTC-05** | Role assignment and checks | Correct role tags for student, faculty, admin | Roles verified: student, faculty, admin | **PASS** | FR9 Verified |
| **UTC-06** | Student-User 1:1 foreign key relationship | Linked user profile matches student | Student profile linked to user `test_student1` | **PASS** | Exp 5 Schema |
| **UTC-07** | AcademicRecord feature extraction dictionary | Dict contains 5 ML feature keys | 5 numeric keys extracted correctly | **PASS** | FR2 Verified |
| **UTC-08** | ML Model metadata storage in DB | Stored model has accuracy and version | Version `v1.0.0` loaded with 87% accuracy | **PASS** | NFR6 Verified |
| **UTC-09** | Prediction CSS badge class generation | CSS classes: danger, warning, success | Mapped correctly to Low, Medium, High | **PASS** | NFR3 Verified |
| **UTC-10** | Preprocessing valid academic features | Clean dict returned with zero errors | Clean values returned; errors=None | **PASS** | FR3 Verified |
| **UTC-11** | Preprocessing missing and empty values | Imputed with default academic baselines | Missing attendance defaulted to 75.0% | **PASS** | FR3 Verified |
| **UTC-12** | Preprocessing out-of-bound feature values | Out of bounds clipped; errors reported | 120% clipped to 100%; error message recorded | **PASS** | Negative test |
| **UTC-13** | Feature conversion to 2D numpy matrix | Shape equals (1, 5) float32 | Matrix shape (1, 5) float32 confirmed | **PASS** | FR3 Verified |
| **UTC-14** | ML classification of weak student profile | Classified as 'High' Risk (score > 0.65) | Risk='High', Score=0.9976 | **PASS** | FR4 Verified |
| **UTC-15** | ML classification of strong student profile | Classified as 'Low' Risk (score < 0.40) | Risk='Low', Score=0.0821 | **PASS** | FR4 Verified |
| **UTC-16** | Factor explainability for attendance < 60% | Flagged as 'Critical' with contribution > 0.30 | Attendance flagged Critical (+0.40 contribution) | **PASS** | FR5 Verified |
| **UTC-17** | ML model inference latency | Latency under 100 milliseconds per record | Mean duration: 4.2ms (<100ms requirement) | **PASS** | NFR4 Verified |
| **UTC-18** | End-to-end single student prediction service | Stored prediction with factors & suggestions | Prediction saved to DB with 4 factors and suggestions | **PASS** | FR4, FR5, FR7 |
| **ITC-01** | Faculty login and dashboard access | Session established, dashboard rendered | Redirected to `/faculty/dashboard` (HTTP 200) | **PASS** | FR1, FR6 |
| **ITC-02** | Filter student roster by High Risk | Only High risk students displayed | Filtered table contains High risk students | **PASS** | FR6 Verified |
| **ITC-03** | Filter student roster by Low Risk | Only Low risk students displayed | Filtered table contains Low risk students | **PASS** | FR6 Verified |
| **ITC-04** | Academic record manual form entry | Record saved and ML prediction generated | Record committed; flash success message displayed | **PASS** | FR2, FR4 |
| **ITC-05** | Batch CSV upload workflow | 2 CSV records ingested and predicted | Ingested 2 records; flash success shown | **PASS** | FR2, FR4 |
| **ITC-06** | Student login and self-service dashboard | Personal risk standing and metrics rendered | Student portal loaded with Roll `TEST001` (HTTP 200) | **PASS** | FR7 Verified |
| **ITC-07** | Privacy isolation: Student access to faculty routes | Access denied flash; redirected to student portal | Redirected with "Access denied" message (HTTP 200) | **PASS** | FR9, NFR2 |
| **ITC-08** | Student notification alerts workflow | Notification list rendered with timestamps | Alerts rendered at `/student/notifications` | **PASS** | Elicited Need |
| **ITC-09** | Admin / HOD dashboard access | Department overview rendered | Dashboard loaded with enrolled metrics (HTTP 200) | **PASS** | FR8 Verified |
| **ITC-10** | Admin department academic report | Printable academic report generated | Academic roster report rendered (HTTP 200) | **PASS** | FR11 Verified |
| **ITC-11** | API unread notifications count | Returns JSON with integer count | JSON `{"unread_count": 0}` received (HTTP 200) | **PASS** | API Verified |

---

## 3. Defect Log (Table 11.4)

During initial integration, the following real defects were detected, logged, and resolved:

| Defect ID | Description | Severity | Module | Root Cause | Status | Resolution |
|---|---|---|---|---|---|---|
| **BUG-01** | `AttributeError: 'function' object has no attribute 'configure'` in `app/db.py` | High | `app/db.py` | In SQLAlchemy 2.0, `scoped_session` with lambda was misconfigured for configure() | **FIXED** | Reconfigured `scoped_session` directly with `sessionmaker` factory |
| **BUG-02** | `SyntaxError: f-string expression part cannot include a backslash` in `ml/evaluate_model.py` | Medium | `ml/evaluate_model.py` | Python 3.11 disallows backslash inside `{...}` in f-strings | **FIXED** | Extracted label string to standalone variable `header_label` |

---

## 4. Test Conclusion
The AI-Based Student Performance Prediction and Early Warning System has successfully passed 100% of unit and integration test scenarios. All core functionalities—including secure authentication, relational schema constraints, machine learning inference, explainability factor calculation, early warning notifications, and role-based data isolation—are verified operational and production-ready for laboratory evaluation.
