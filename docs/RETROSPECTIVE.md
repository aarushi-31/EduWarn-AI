# Project Retrospective & Post-Mortem Analysis
## AI-Based Student Performance Prediction and Early Warning System
**Department of CSE (AIML), JSS University, Noida**  
**Course**: B.Tech 5th Sem | **Lab**: Software Engineering Lab (JCSAIMLL-001)  
**Experiment Reference**: Experiment 12

---

## 1. What went well during project development?
- **Seamless 5-Layer Architectural Separation**: Decoupling the presentation layer from backend routes, business logic, data access, and machine learning pipelines allowed different members of the team to work on their respective domains without stepped-on toes or architectural spaghetti.
- **Genuine ML Model Comparison & Explainability**: Rather than hardcoding predictions, we built a reproducible pipeline that compared Logistic Regression, Decision Tree, and Random Forest, selected the champion model (87.08% accuracy, 86.00% macro F1), and persisted the full pipeline artifact.
- **Relational Integrity**: Implementing the 14-table 3NF schema designed in Experiment 5 provided clean relational foreign keys, cascade rules, and audit trails.
- **Comprehensive Test Suite**: Achieving 100% pass rate across 29 unit and integration tests gave high confidence in software reliability.

---

## 2. What difficulties occurred during requirements analysis, design, coding, or testing?
- **Balancing Accuracy vs. Explainability**: Complex non-linear models like deep trees can act as black boxes. For academic decision-support, faculty require transparency into *why* a student was flagged. We resolved this by combining calibrated class probabilities with explicit feature attribution weights.
- **Cross-Cycle Risk Transitions**: Capturing when a student shifts from Low Risk in IA-1 to High Risk in IA-2 required comparing historical cycles in database queries without impacting web response latency.
- **Cross-Platform Compatibility**: Ensuring path separators and SQLite file locks behaved reliably across Windows and Linux CI environments required using `os.path.join` and relative paths throughout.

---

## 3. How were integration and collaboration issues handled?
- **Contract-First Development**: We established the database schema (`database/schema.sql`) and feature contracts (`ml/preprocessing.py`) as foundational constants before building the user interface or API controllers.
- **Conventional Branching & Review Protocol**: Clear ownership of modules across the 4 team members prevented merge conflicts. Pull requests were reviewed using our standardized checklist.

---

## 4. Which tools and practices were most useful?
- **PyTest**: The automated test suite allowed rapid regression detection after refactoring database models and inference routines.
- **Bootstrap 5 & Chart.js**: Enabled clean, responsive, role-based dashboards with zero frontend framework overhead (avoiding complex Node/npm build dependencies).
- **SQLAlchemy 2.0 ORM**: Provided object-relational mapping while maintaining strict SQL check constraints and foreign keys.

---

## 5. What did the team learn about version control, testing, and documentation?
- **Version Control**: Feature branching and conventional commit messages transform Git from a simple backup mechanism into an auditable project journal.
- **Testing**: Writing positive, negative, and boundary tests for preprocessing prevented data leakage and server crashes on malformed inputs.
- **Traceability**: Building a Requirements Traceability Matrix (RTM) ensures that every customer requirement in the SRS is backed by real code and verifiable tests.

---

## 6. What would the team improve if the project were developed again?
- **Automated Email/SMS Alerts**: Integrate an institutional SMTP or SMS gateway to dispatch automated early warning alerts directly to parents and mentors.
- **LMS Integration**: Build LTI (Learning Tools Interoperability) connectors to directly ingest attendance and marks from platforms like Moodle or Canvas.
- **Time-Series Deep Learning**: Explore LSTM / GRU recurrent architectures to model week-by-week attendance trajectories across an entire four-year degree program.
