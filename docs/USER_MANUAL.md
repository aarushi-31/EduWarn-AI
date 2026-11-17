# User Manual & Operational Handbook
## AI-Based Student Performance Prediction and Early Warning System
**Department of CSE (AIML), JSS University, Noida**  
**Course**: B.Tech 5th Sem | **Lab**: Software Engineering Lab (JCSAIMLL-001)  
**Experiment Reference**: Experiment 12

---

## 1. Introduction & System Overview
The **AI-Based Student Performance Prediction and Early Warning System (EduWarn AI)** is an intelligent web application designed to support faculty, academic heads, and students in higher education. It continuously monitors academic indicators—such as attendance percentage, internal examination marks, assignment scores, classroom participation, and prior semester performance—to identify students at risk of academic failure before semester examinations.

### Key Capabilities
- **Supervised Risk Classification**: Categorizes students into `High Risk` (red), `Medium Risk` (yellow), and `Low Risk` (green).
- **Explainable AI (XAI)**: Identifies the exact contributing features (e.g. low attendance, missed assignments) behind each prediction.
- **Actionable Guidance**: Delivers evidence-based suggestions to help students restore academic standing.
- **Early Warning Alerts**: Detects when a student's risk level escalates between cycles and immediately dispatches alerts to both the student and their teacher.
- **Strict Role-Based Privacy**: Ensures students can only view their own private evaluations.

---

## 2. System Requirements & Access
- **Supported Browsers**: Google Chrome (v90+), Mozilla Firefox (v88+), Microsoft Edge (v90+), Apple Safari.
- **Local Application URL**: `http://127.0.0.1:5000/`
- **Supported Display**: Responsive across laptop screens, tablets, and smartphones.

---

## 3. Getting Started & Logging In

1. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```
2. You will be greeted by the **Sign In** screen.
3. For academic lab evaluation, click any of the **Quick Demo Credentials** buttons at the bottom of the card to automatically fill credentials:
   - **Faculty Member**: `faculty_neha` / `FacultyPassword123!`
   - **Student (High Risk)**: `student_rohit` / `StudentPassword123!`
   - **Student (Low Risk)**: `student_aarav` / `StudentPassword123!`
   - **Department Head (HOD)**: `admin_hod` / `AdminPassword123!`
4. Click **Sign In**.

---

## 4. Faculty Portal Guide

### 4.1 Dashboard Overview
Upon logging in as faculty, you arrive at the **Faculty Academic Monitoring Dashboard**:
- **Metric Cards**: Display total monitored students and counts for High Risk, Medium Risk, and Low Risk students.
- **Class & Cycle Selectors**: Filter your view by assigned class (e.g., Sem 5 Sec A) and assessment cycle (IA-1, IA-2).
- **Risk Filter Buttons**: Instantly filter the roster by clicking **High**, **Medium**, **Low**, or **All**.
- **Search Bar**: Type any part of a student's roll number or name to search immediately.

### 4.2 Inspecting a Student's Detailed Analysis
1. In the student table, locate the student you wish to inspect.
2. Click the **View Analysis** button in the rightmost column.
3. The **Student Academic Analysis** screen displays:
   - **Predicted Standing Banner**: High/Medium/Low badge with continuous risk index.
   - **Key Contributing Factors Table (FR5)**: Lists which academic features contributed most heavily to the prediction (e.g., Attendance: Critical +0.40).
   - **Actionable Improvement Guidance (FR7)**: Specific recommendations tailored to this student's weakest areas.
   - **Cycle Progression Table & Graph**: Historical comparison between IA-1, IA-2, and trends over time.

### 4.3 Entering Marks Manually (FR2)
1. Click **Enter Marks** in the top navigation bar.
2. Select the **Class**, **Subject**, and **Assessment Cycle**.
3. Select the student from the roster dropdown.
4. Input the academic parameters:
   - Attendance % (0.0 to 100.0)
   - Internal Exam Marks (0.0 to 30.0)
   - Assignment Score (0.0 to 25.0)
   - Participation Score (0.0 to 20.0)
   - Previous Semester % (0.0 to 100.0)
5. Click **Save Record & Run ML Inference**. The system saves the record and immediately updates the prediction.

### 4.4 Bulk CSV Upload (FR2)
1. Click **Upload CSV** in the top navigation bar.
2. Click **Download Sample CSV Template** to review the required column headers (`roll_no`, `attendance_pct`, `internal_marks`, `assignment_score`, `participation_score`, `prev_sem_marks`).
3. Select the target **Subject** and **Assessment Cycle**.
4. Choose your completed CSV file and click **Upload & Process Predictions**.
5. A confirmation message displays the total records imported and predictions generated.

---

## 5. Student Portal Guide

### 5.1 Personal Academic Standing (FR7)
1. Log in with your student credentials (e.g., `student_rohit` / `StudentPassword123!`).
2. The **Student Academic Self-Service Portal** displays:
   - Your official **Predicted Academic Standing** badge.
   - Color-coded indicator cards for Attendance %, Internal Marks, Assignments, and Previous Semester standing.
   - **Why Did AI Predict This Risk Level?**: An explainability card showing which factors are pulling your risk score up or down.
   - **Recommended Action Plan**: Concrete guidance (e.g., "Prioritize attending the next 14 consecutive lectures/labs to cross the 75% threshold").
   - **Historical History Table**: Track your progress between IA-1 and IA-2.

### 5.2 Checking Early Warning Alerts
1. Click the **Alerts (Bell)** icon in the navigation bar.
2. If your risk status changed (e.g., from Low to Medium or Medium to High), an automated early warning notification will appear detailing the transition.
3. Click **Mark Read** once reviewed.

---

## 6. Administrator / HOD Portal Guide

### 6.1 Department Overview (FR8)
1. Log in with HOD credentials (`admin_hod` / `AdminPassword123!`).
2. The **HOD Department Overview** displays:
   - Enrolled student count, total faculty, and class sections.
   - **Risk Category Distribution Chart**: Interactive doughnut chart summarizing department-wide risk.
   - **Active ML Model Governance Card**: Auditable metadata showing algorithm, version (`v1.0.0`), validation accuracy (87.08%), and macro F1-score (86.00%).
   - **Class-Level Breakdown Table**: Comparing Section A vs Section B risk counts.

### 6.2 Generating Department Reports (FR11)
1. Click **Department Reports** in the navigation bar.
2. Select the desired **Assessment Cycle**.
3. Review the complete student roster with risk indices and recommended academic interventions.
4. Click **Print / Export PDF** to generate an official laboratory practical report or hardcopy for departmental meetings.

---

## 7. Troubleshooting & FAQ

| Problem | Likely Cause | Solution |
|---|---|---|
| **Cannot log in ("Invalid credentials")** | Incorrect password or username typo | Use the one-click demo credentials pills on `/auth/login` |
| **"Access denied" message** | Attempting to access faculty or admin route with student account | Log out and log in with an authorized faculty or admin account |
| **Attendance warning indicator** | Attendance is below 75.0% | System flags mandatory university detention risk under 75% |
| **CSV upload reports student not found** | Roll number does not exist in database | Verify roll number spelling against the student roster table |
