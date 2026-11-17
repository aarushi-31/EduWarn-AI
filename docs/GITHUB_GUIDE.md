# Git & GitHub Collaboration Guide
## AI-Based Student Performance Prediction and Early Warning System
**Department of CSE (AIML), JSS University, Noida**  
**Course**: B.Tech 5th Sem | **Lab**: Software Engineering Lab (JCSAIMLL-001)  
**Experiment Reference**: Experiment 9

---

## 1. Git Repository Configuration

### 1.1 Initial Setup
Configure your Git username and institutional email before making commits:
```powershell
git config --global user.name "Your Full Name"
git config --global user.email "your.roll@jssuni.edu.in"
```

### 1.2 Repository Structure
The repository uses the standard Git branch topology:
- **`main`**: Production-ready branch containing only verified, tested releases.
- **`develop`**: Central integration branch for ongoing sprint development.
- **`feature/<name>`**: Feature branches branched from `develop` and merged via Pull Requests.

---

## 2. Four-Member Step-by-Step Workflow

### Member 1: Frontend & Templates
```powershell
git checkout develop
git checkout -b feature/ui-dashboards
# Work on app/templates/ and app/static/
git add app/templates/ app/static/
git commit -m "feat(ui): implement responsive faculty and student dashboard templates"
git push origin feature/ui-dashboards
```

### Member 2: Backend & Authentication
```powershell
git checkout develop
git checkout -b feature/auth-controllers
# Work on app/routes/auth.py and app/services/auth_service.py
git add app/routes/auth.py app/services/auth_service.py
git commit -m "feat(auth): implement session login, registration, and RBAC decorators"
git push origin feature/auth-controllers
```

### Member 3: Machine Learning & Inference
```powershell
git checkout develop
git checkout -b feature/ml-training-pipeline
# Work on ml/
git add ml/
git commit -m "feat(ml): train model comparison suite and serialize champion pipeline"
git push origin feature/ml-training-pipeline
```

### Member 4: Database, Testing & CI/CD
```powershell
git checkout develop
git checkout -b feature/database-and-tests
# Work on database/ and tests/
git add database/ tests/ .github/
git commit -m "feat(test): add 29-test pytest suite and GitHub Actions workflow"
git push origin feature/database-and-tests
```

---

## 3. Pull Request & Code Review Procedure

1. **Pre-PR Verification**: Run all unit and integration tests locally before opening a PR:
   ```powershell
   pytest -v
   ```
   Do not open a PR if any test fails!
2. **Opening the PR on GitHub**:
   - Set base branch to `develop`.
   - Title: Follow Conventional Commits format (e.g. `feat(ml): add explainability factor calculation`).
   - Describe changes made and link to relevant SRS functional requirements (e.g. FR4, FR5).
3. **Peer Review Checklist**:
   - [ ] No hardcoded passwords or API secrets in code.
   - [ ] All inputs properly validated (bounds checked).
   - [ ] Student data isolation preserved (no cross-user data leakage).
   - [ ] Automated tests added for newly introduced functions.
   - [ ] CI pipeline builds and tests pass cleanly on both Linux and Windows.
4. **Merging**:
   - Squash and merge (or merge commit) into `develop`.
   - Delete the remote feature branch after merge.
