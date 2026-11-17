# Lab File Screenshots & Evidence Checklist
## Software Engineering Lab (JCSAIMLL-001) - Experiments 6 to 13
**Department of CSE (AIML), JSS University, Noida**

This checklist details the exact evidence and screenshots to capture during actual system execution for your laboratory practical file.

---

| Item # | Experiment Ref | Required Screenshot / Evidence Description | Exact URL / Terminal Command to Run | Expected Output / Content to Highlight | Captured? |
|---|---|---|---|---|---|
| **SS-01** | Exp 6 & 7 | **Application Login Page** | `http://127.0.0.1:5000/auth/login` | Clean login form with role selector / demo credentials hint | [ ] |
| **SS-02** | Exp 6 & 7 | **Faculty Dashboard (Overview & Metrics)** | `http://127.0.0.1:5000/faculty/dashboard` | Assigned classes, total students, risk distribution overview | [ ] |
| **SS-03** | Exp 6 & 7 | **Faculty Student Roster (Filtered by High Risk)** | `http://127.0.0.1:5000/faculty/dashboard?risk=High` | Table showing only students flagged with High Risk and red badges | [ ] |
| **SS-04** | Exp 6 & 7 | **Student Academic Detail & Factor Explainability** | `http://127.0.0.1:5000/faculty/student/1` | Contributing risk factors breakdown, attendance chart, history | [ ] |
| **SS-05** | Exp 6 & 7 | **Academic Data Entry Form** | `http://127.0.0.1:5000/faculty/enter-record` | Form with inputs for Attendance, Internal Marks, Assignments | [ ] |
| **SS-06** | Exp 6 & 7 | **Batch CSV Upload & Immediate Prediction** | `http://127.0.0.1:5000/faculty/upload-csv` | CSV upload box and success confirmation of processed records | [ ] |
| **SS-07** | Exp 6 & 7 | **Student Self-Service Dashboard** | `http://127.0.0.1:5000/student/dashboard` | Student personal view showing current risk level and recommendations | [ ] |
| **SS-08** | Exp 6 & 7 | **Early Warning Notification Alert** | Student / Faculty notification bell dropdown | Risk change alert (e.g. "Risk increased from Low to Medium") | [ ] |
| **SS-09** | Exp 6 & 7 | **Admin / HOD Department Aggregate Dashboard** | `http://127.0.0.1:5000/admin/dashboard` | Department summary cards, class-wise distribution, Chart.js pie chart | [ ] |
| **SS-10** | Exp 5 & 6 | **Database Tables & Seed Verification** | `python database/init_db.py --status` or SQLite CLI | Display 14 relational tables with populated records | [ ] |
| **SS-11** | Exp 6 & 7 | **ML Model Comparison & Training Output** | `python ml/train_model.py` | Terminal output showing Logistic Regression, Decision Tree, Random Forest metrics | [ ] |
| **SS-12** | Exp 6 & 7 | **ML Evaluation Confusion Matrix & Metrics** | `python ml/evaluate_model.py` | Accuracy, Precision, Recall, Macro F1, classification report | [ ] |
| **SS-13** | Exp 8 & 11| **PyTest Unit Tests Execution** | `pytest tests/unit -v` | Green passing output for auth, preprocessing, models, and service | [ ] |
| **SS-14** | Exp 8 & 11| **PyTest Integration Tests Execution** | `pytest tests/integration -v` | Green passing output for full end-to-end user workflows | [ ] |
| **SS-15** | Exp 9 | **Git Local Repository Status & Branches** | `git branch -a; git status` | Shows `main`, `develop`, and `feature/*` branches | [ ] |
| **SS-16** | Exp 9 | **Git Commit History Graph** | `git log --graph --oneline -n 15` | Clean conventional commits demonstrating incremental team work | [ ] |
| **SS-17** | Exp 10 | **GitHub Actions CI Workflow Configuration** | Inspect `.github/workflows/tests.yml` | Workflow YAML showing Python setup, test execution, and caching | [ ] |
| **SS-18** | Exp 13 | **Live Practical Demonstration Walkthrough** | Complete live execution on Windows laptop | Multi-role browser demonstration before faculty evaluator | [ ] |
