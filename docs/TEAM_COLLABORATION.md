# Team Collaboration Guide
## AI-Based Student Performance Prediction and Early Warning System
**Department of CSE (AIML), JSS University, Noida**  
**Team of 4 Third-Year B.Tech Students | Semester 5**

---

## 1. Team Composition & Module Ownership

| Member | Designated Role | Primary Modules Owned | Core Code & Artifact Ownership |
|---|---|---|---|
| **Member 1** | **Frontend & UI/UX Specialist** | Presentation Layer, Dashboard Views, Visualizations | `app/templates/`, `app/static/css/`, `app/static/js/`, Chart.js integrations, UI responsiveness |
| **Member 2** | **Backend & Security Engineer** | Application Layer, Authentication, Routing, RBAC | `app/routes/`, `app/services/auth_service.py`, `app/config.py`, Session state & security decorators |
| **Member 3** | **AI/ML & Data Science Engineer** | Machine Learning Layer, Dataset, Inference Engine | `ml/`, `app/services/prediction_service.py`, `app/services/explainability.py`, model training & evaluation |
| **Member 4** | **Database, QA & DevOps Lead** | Data Access & Storage Layer, Testing, CI/CD, Docs | `database/`, `app/models/`, `tests/`, `.github/workflows/`, test execution and lab documentation |

---

## 2. Git Branching Model

We follow a structured Git Feature Branch Workflow:

- **`main`**: The single source of truth. Contains only fully tested, peer-reviewed, and verified code.
- **`develop`**: The shared integration branch where tested features converge before lab submission.
- **`feature/<module-name>`**: Dedicated short-lived branches created off `develop` for specific tasks.

### Standard Branch Naming Conventions
- `feature/auth-and-rbac` (Member 2)
- `feature/database-schema-and-seed` (Member 4)
- `feature/ml-model-training` (Member 3)
- `feature/faculty-student-dashboards` (Member 1)
- `feature/early-warning-service` (Member 3)
- `feature/pytest-test-suite` (Member 4)
- `feature/github-actions-ci` (Member 4)
- `bugfix/<issue-description>`
- `docs/<document-name>`

---

## 3. Commit Message Conventions

We adhere to the **Conventional Commits** specification:
```
<type>(<scope>): <short descriptive summary in imperative mood>

[optional detailed body]
[optional issue reference]
```

### Commit Types
- `feat`: A new user-facing or technical feature
- `fix`: A bug fix
- `docs`: Documentation updates only
- `test`: Adding or refactoring automated tests
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `style`: Changes that do not affect code logic (formatting, CSS spacing)
- `chore`: Build process, dependencies, or tool configurations

### Examples:
- `feat(auth): implement PBKDF2 password hashing and role-based session check`
- `feat(ml): train Random Forest classifier on academic dataset with 92% F1-score`
- `fix(faculty): resolve student risk filter dropdown query parameters`
- `test(integration): add end-to-end faculty academic record upload test`
- `docs(rtm): update requirements traceability matrix for FR1-FR11`

---

## 4. Pull Request & Code Review Process

1. **Local Pre-Check**: Before opening a Pull Request, the author must execute:
   ```powershell
   pytest
   ```
   All tests must pass locally with zero regressions.
2. **Opening the PR**:
   - Push feature branch: `git push origin feature/<module-name>`
   - Target branch: `develop` (or `main` for milestone releases).
   - Title: Follow conventional commit format.
   - PR Description: Must state:
     - What was changed.
     - Which requirements (FR/NFR) are addressed.
     - Steps to manually verify.
     - Evidence of passing test suite.
3. **Peer Review Rules**:
   - At least one other team member must review and approve the PR.
   - Code Review Checklist:
     - [ ] Are variable and function names self-descriptive?
     - [ ] Are sensitive variables (e.g. `SECRET_KEY`) kept in environment configs, not hardcoded?
     - [ ] Are input validations in place (preventing negative marks or attendance > 100%)?
     - [ ] Is student privacy preserved (no leaking data between student accounts)?
     - [ ] Are unit/integration tests included for newly added logic?
     - [ ] Do all automated tests pass without errors?

---

## 5. Sequential Merge Order for Core Implementation

To avoid merge conflicts, modules must be merged in dependency order:
1. **Step 1**: Foundation & Database (`database/`, `app/models/`) -> Merged by Member 4.
2. **Step 2**: ML Pipeline & Artifact (`ml/`) -> Merged by Member 3.
3. **Step 3**: Authentication & Core Services (`app/routes/auth.py`, `app/services/`) -> Merged by Member 2.
4. **Step 4**: Presentation & UI Dashboards (`app/templates/`, `app/static/`) -> Merged by Member 1.
5. **Step 5**: Test Suite & CI Automation (`tests/`, `.github/workflows/`) -> Merged by Member 4.
6. **Step 6**: Final Integration & Lab Record Verification -> All 4 Members.
