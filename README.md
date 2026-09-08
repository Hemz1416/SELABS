# Software Engineering Laboratory (UE22CS351AA2)
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
└── Lab3/    # Component Modelling & Architectural Pattern Selection
    ├── README.md
    ├── PES2UG24CS192_Lab_3.pdf
    ├── Analysis/
    │   └── Lab3_Architecture_Analysis.md
    ├── Diagram/
    │   ├── Lab3_Alumni_Mentorship_Component_Diagram.puml
    │   ├── Lab3_Alumni_Mentorship_Component_Diagram.png
    │   └── Lab3_Alumni_Mentorship_Component_Diagram.pdf
    └── Documentation/
        ├── Lab3_Alumni_Mentorship_Architectural_Justification.docx
        ├── Lab3_Alumni_Mentorship_Architectural_Justification.pdf
        └── PES2UG24CS192_Lab_3.pdf
```

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
