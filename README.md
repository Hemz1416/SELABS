# Software Engineering Laboratory

**Department of Computer Science and Engineering — PES University**

| Student Information | Details |
| :--- | :--- |
| **Student Name** | HEMANT RAM NELAPATI |
| **SRN** | PES2UG24CS192 |
| **Section / Track** | 5th Sem — Section D / Orange Track |
| **Assigned Domain** | Campus & Academic Operations |
| **Assigned Scenario** | Problem Statement #06: Alumni Mentorship & Mock Interview Platform |

---

## Repository Structure

```
SELABS/
├── README.md
├── Lab1/    # Requirements Engineering & UML Use-Case Modelling
├── Lab2/    # Agile Project Management & Scrum Sprints in Jira
├── Lab3/    # Component Modelling & Architectural Pattern Selection
└── Lab5/    # Static Code Analysis (Pylint, Bandit, Flake8)
    ├── PES2UG24CS192_Lab5.pdf
    ├── README.md
    ├── helpdesk_system.py
    ├── issues.md
    ├── reflection.md
    ├── pylint_report.txt
    ├── bandit_report.txt
    └── flake8_report.txt
```

---

## Lab 5: Static Code Analysis (Pylint, Bandit, Flake8)

### 1. Overview & Assigned Scenario
- **Assigned Scenario**: Problem Statement #06 — IT Helpdesk Ticket Allocator (`helpdesk_system.py`)
- **Reference Script**: `inventory_system.py` (Student Handout Reference)
- **Scores Achieved**:
  - **Pylint Score**: **10.00 / 10.00** (Perfect Score — Zero warnings, zero conventions, zero errors)
  - **Bandit Score**: **0 Vulnerabilities** (Zero High, Medium, or Low severity issues)
  - **Flake8 Score**: **0 Violations** (100% PEP 8 compliance)

### 2. Lab 5 Deliverables
- **Official Submission Report (PDF)**: [`PES2UG24CS192_Lab5.pdf`](Lab5/PES2UG24CS192_Lab5.pdf)
- **Refactored Helpdesk System**: [`helpdesk_system.py`](Lab5/helpdesk_system.py)
- **Refactored Inventory System**: [`inventory_system.py`](Lab5/inventory_system.py)
- **Static Analysis Issue Log**: [`issues.md`](Lab5/issues.md)
- **Reflection & Answers**: [`reflection.md`](Lab5/reflection.md)
- **Verification Reports**:
  - Pylint Report: [`pylint_report.txt`](Lab5/pylint_report.txt)
  - Bandit Report: [`bandit_report.txt`](Lab5/bandit_report.txt)
  - Flake8 Report: [`flake8_report.txt`](Lab5/flake8_report.txt)

---

## Lab 3: Component Modelling & Architectural Pattern Selection

### 1. Selected Architecture
**Layered (Three-Tier) Architecture**
- **Presentation Tier**: Student Mentee Portal, Alumni Mentor Portal
- **Business Logic Tier**: Authentication & User Management, Mentorship & Mock Interview Management, Notification Service
- **Data Persistence Tier**: Database Access (Relational DB / ORM)

### 2. Components & Interfaces Summary

| Component Name | Tier | Provided Interfaces | Required Interfaces |
| :--- | :--- | :--- | :--- |
| **Student Mentee Portal** | Presentation | — | `IAuthentication`, `IUserProfile`, `IMentorshipService`, `IInterviewScheduling` |
| **Alumni Mentor Portal** | Presentation | — | `IAuthentication`, `IUserProfile`, `IMentorshipService`, `IInterviewScheduling` |
| **Authentication & User Management** | Business Logic | `IAuthentication`, `IUserProfile` | `IDataAccess` |
| **Mentorship & Mock Interview Management** | Business Logic | `IMentorshipService`, `IInterviewScheduling` | `IDataAccess`, `INotification` |
| **Notification Service** | Business Logic | `INotification` | `IDataAccess` |
| **Database Access** | Data Persistence | `IDataAccess` | — (Relational DB Engine) |

### 3. Lab 3 Deliverables
- **Submission Document**: [`PES2UG24CS192_Lab_3.pdf`](Lab3/PES2UG24CS192_Lab_3.pdf)
- **Component Diagram (PNG)**: [`Lab3_Alumni_Mentorship_Component_Diagram.png`](Lab3/Diagram/Lab3_Alumni_Mentorship_Component_Diagram.png)
- **Component Diagram (PDF)**: [`Lab3_Alumni_Mentorship_Component_Diagram.pdf`](Lab3/Diagram/Lab3_Alumni_Mentorship_Component_Diagram.pdf)
- **PlantUML Source**: [`Lab3_Alumni_Mentorship_Component_Diagram.puml`](Lab3/Diagram/Lab3_Alumni_Mentorship_Component_Diagram.puml)
- **Architectural Justification (Word)**: [`Lab3_Alumni_Mentorship_Architectural_Justification.docx`](Lab3/Documentation/Lab3_Alumni_Mentorship_Architectural_Justification.docx)
- **Architectural Analysis**: [`Lab3_Architecture_Analysis.md`](Lab3/Analysis/Lab3_Architecture_Analysis.md)
