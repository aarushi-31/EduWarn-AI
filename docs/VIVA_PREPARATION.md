# Practical Examination & Viva Voce Preparation Guide
## AI-Based Student Performance Prediction and Early Warning System
**Department of CSE (AIML), JSS University, Noida**  
**Course**: B.Tech 5th Sem | **Lab**: Software Engineering Lab (JCSAIMLL-001)  
**Experiment Reference**: Experiment 13

---

## 1. Live Demonstration Sequence for Examiners

When called for the practical exam demonstration, follow this exact 5-step walkthrough:

### Step 1: Launch Application & Verify Tests (Terminal)
1. Open PowerShell and run automated tests to show examiners that all 29 tests pass:
   ```powershell
   pytest -v
   ```
2. Start the web application:
   ```powershell
   python run.py
   ```
3. Open browser at: `http://127.0.0.1:5000/`

### Step 2: Faculty Dashboard Walkthrough
1. On the login screen, click the **Faculty Demo** button (`faculty_neha` / `FacultyPassword123!`).
2. Show the examiner the **Faculty Academic Monitoring Dashboard**:
   - Point out the 4 summary cards: Total Monitored, High Risk (red), Medium Risk (warning), Low Risk (green).
   - Demonstrate the **Risk Filter** buttons: Click **High** to show students at danger; click **Low** to show top performers.
   - Use the **Search Bar** to search for "Rohit".

### Step 3: Explainable AI & Factor Explainability (FR5, FR7)
1. Click **View Analysis** for student **Rohit Sharma (22AIML001)**.
2. Highlight:
   - **Predicted High Risk Badge** with Continuous Risk Score (0.998).
   - **Key Contributing Factors Table (FR5)**: Show that Attendance (52%) and Internal Marks (11.5/30) are flagged as Critical.
   - **Actionable Suggestions (FR7)**: Point out recommendations (e.g. "Attend next 14 consecutive lectures", "Meet academic mentor").
   - **Historical Comparison Chart**: Show the bar graph comparing IA-1 and IA-2 scores.

### Step 4: Academic Record Entry & Instant ML Inference (FR2, FR4)
1. Click **Enter Marks** in the top navigation.
2. Select Class (Sem 5 Sec A), Subject (Software Engineering), Cycle (IA-2).
3. Choose a student and enter experimental values (e.g. Attendance 48%, Internals 9/30).
4. Click **Save Record & Run ML Inference**.
5. Show how the database record updates and the ML model immediately recalculates risk!

### Step 5: Student & Admin Portals
1. Log out, then click **Student Demo** (`student_rohit` / `StudentPassword123!`).
   - Show that Rohit can only view his personal profile (Privacy / NFR2).
   - Show the **Notification Alerts (Bell Icon)** detailing the early warning message.
2. Log out, then click **Admin / HOD Demo** (`admin_hod` / `AdminPassword123!`).
   - Show the **Department Overview Doughnut Chart** and class-wise breakdown.
   - Show the **ML Model Governance Card** detailing algorithm, version, and 87.08% validation accuracy.
   - Open **Department Reports (FR11)** and click **Print / Export PDF** to show report generation.

---

## 2. Core Architecture & Design Defense

### Q1: Why did you choose a 5-layer modular monolith instead of microservices?
**Answer**: For an academic laboratory system, a modular monolith separates concerns (Presentation, Application, Business/ML, Data Access, and Storage) cleanly without the operational complexity, network latency, distributed transactions, and failure modes of microservices. It runs locally with zero infrastructure cost and is easily maintainable by a small engineering team.

### Q2: How does the database design satisfy Third Normal Form (3NF)?
**Answer**:
- **1NF**: All attributes are atomic (e.g., contributing factors are individual rows in `prediction_factors`, not CSV strings).
- **2NF**: All non-key attributes are fully functionally dependent on the entire primary key (subject and cycle definitions are decoupled into separate lookup tables).
- **3NF**: There are no transitive dependencies; non-prime attributes depend only on the primary key (e.g., student name depends on `student_id`, while department info depends on `dept_id`).

### Q3: Why does your model predict Logistic Regression over Random Forest?
**Answer**: During our model comparison experiment (`ml/train_model.py`), we evaluated Logistic Regression, Decision Tree, and Random Forest on 1,200 samples with stratified 80/20 splitting. Logistic Regression achieved 87.08% accuracy and an 86.00% macro F1-score with calibrated class probabilities, and crucially had zero false negatives for High Risk (zero High risk students misclassified as Low risk). It also offers transparent, explainable linear log-odds coefficients essential for academic fairness.

### Q4: How is data privacy enforced between students?
**Answer**: At the application layer, route controllers enforce session-based checks (`@role_required('student')`). Queries are bound strictly to `session['user_id']`. Even if a student manually modifies a URL parameter, the application fetches only the record linked to their authenticated session, preventing Insecure Direct Object References (IDOR).

### Q5: How is continuous integration configured?
**Answer**: We configured a GitHub Actions CI workflow in `.github/workflows/tests.yml`. On every `push` or `pull_request` to `main` or `develop`, it spins up Ubuntu and Windows runners, configures Python 3.11, installs dependencies, initializes the test database, trains the ML pipeline, and runs all 29 PyTest automated tests.

---

## 3. Top 20 Common Viva Voce Questions & Answers

| # | Question | Concise Technical Answer |
|---|---|---|
| **1** | What is an SRS? | A Software Requirements Specification is a formal document defining functional and non-functional requirements and operational constraints of a software system. |
| **2** | What is the difference between Functional and Non-Functional Requirements? | Functional requirements specify what behaviors the system must perform (e.g. FR4 risk prediction). Non-functional requirements specify quality attributes like security, latency, and maintainability. |
| **3** | What UML diagrams did you prepare in Experiment 3? | Use Case Diagram (actor interactions), Class Diagram (static object structure), Activity Diagram (business workflows), and Sequence Diagram (chronological message calls). |
| **4** | What is an `<<include>>` vs `<<extend>>` relationship in Use Case diagrams? | `<<include>>` represents mandatory supporting behavior (e.g., Predict Risk includes Preprocess Data). `<<extend>>` represents optional/conditional behavior (e.g., Notify Risk Change extends Predict Risk). |
| **5** | How do you prevent SQL Injection? | By utilizing SQLAlchemy ORM and parameterized SQL queries where inputs are passed as parameters rather than concatenated directly into SQL strings. |
| **6** | How are user passwords secured? | Passwords are never stored in plaintext; they are hashed with cryptographic salt using Werkzeug's PBKDF2 with SHA-256 (or Scrypt). |
| **7** | What features does your ML model use? | Five features: Attendance %, Internal Marks, Assignment Score, Classroom Participation Score, and Previous Semester %. |
| **8** | What is data leakage and how did you prevent it? | Data leakage occurs when test information contaminates model training. We prevented it by performing stratified train-test splitting before fitting our `StandardScaler` pipeline. |
| **9** | What is Macro F1-score and why use it instead of accuracy? | Accuracy can be misleading on imbalanced datasets. Macro F1 calculates the unweighted mean of F1-scores across all three risk classes (High, Medium, Low), ensuring minority classes are evaluated fairly. |
| **10** | What is Explainable AI (XAI) in your system? | Rather than giving only a black-box risk label, the system computes feature contribution factors and translates them into understandable diagnostics and recommendations. |
| **11** | What is an assessment cycle? | An academic milestone (e.g., IA-1, IA-2) used to track student performance trends over time and trigger early warnings upon negative transitions. |
| **12** | What is Unit Testing? | Testing individual software units or functions in complete isolation from the rest of the application. |
| **13** | What is Integration Testing? | Testing the interactions and communication between multiple connected modules (e.g. CSV upload + DB persistence + ML prediction). |
| **14** | What is Continuous Integration? | A software engineering practice where code changes are automatically built, validated, and tested upon pushing to version control. |
| **15** | What is the purpose of `.gitignore`? | It specifies files and directories that Git should ignore and not commit to version control, such as virtual environments (`.venv`), bytecode (`__pycache__`), and local databases. |
| **16** | What is a Pull Request (PR)? | A mechanism to propose changes from a feature branch to an integration branch, allowing code review and CI verification before merging. |
| **17** | What is 3NF in database normalization? | A database is in 3NF if it is in 2NF and has no transitive dependencies (non-prime attributes must depend solely on the primary key). |
| **18** | What does ACID stand for? | Atomicity, Consistency, Isolation, and Durability—the four fundamental properties guaranteeing reliable database transactions. |
| **19** | How does the Early Warning System notify users? | When a newly computed prediction differs from a student's prior cycle prediction, an alert record is created in the `notifications` table for both the student and their teacher. |
| **20** | How can this project be scaled in the future? | By extracting the prediction service into a containerized microservice, connecting an external PostgreSQL database, and integrating with institutional LMS platforms like Canvas or Moodle via LTI APIs. |
