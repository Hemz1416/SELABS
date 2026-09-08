# Lab 3 – Component Modelling & Architectural Pattern Selection

**Project:** Alumni Mentorship & Mock Interview Platform  
**Student:** HEMANT RAM NELAPATI  
**SRN:** PES2UG24CS192  
**Domain:** Campus & Academic Operations  
**Actors:** Student Mentee, Alumni Mentor

---

## Selected Architecture

**Layered (Three-Tier) Architecture**

The system is organised into three layers:
- **Presentation Layer** — Student and Alumni portals
- **Business Logic Layer** — Authentication, Mentorship/Interview Management, Notifications
- **Data Layer** — Centralised database access

## Components (6)

| # | Component | Layer |
|---|-----------|-------|
| 1 | Student Mentee Portal | Presentation |
| 2 | Alumni Mentor Portal | Presentation |
| 3 | Authentication & User Management | Business Logic |
| 4 | Mentorship & Mock Interview Management | Business Logic |
| 5 | Notification Service | Business Logic |
| 6 | Database Access | Data |

## Interfaces (6)

| # | Interface | Provided By | Required By |
|---|-----------|-------------|-------------|
| 1 | IAuthentication | Auth & User Mgmt | Student Portal, Alumni Portal |
| 2 | IUserProfile | Auth & User Mgmt | Student Portal, Alumni Portal |
| 3 | IMentorshipService | Mentorship & Interview Mgmt | Student Portal, Alumni Portal |
| 4 | IInterviewScheduling | Mentorship & Interview Mgmt | Student Portal, Alumni Portal |
| 5 | INotification | Notification Service | Mentorship & Interview Mgmt |
| 6 | IDataAccess | Database Access | Auth, Mentorship Mgmt, Notification Service |

## Deliverables

```
Lab3/
├── README.md
├── Diagram/
│   ├── Lab3_Alumni_Mentorship_Component_Diagram.puml   (editable source)
│   ├── Lab3_Alumni_Mentorship_Component_Diagram.png    (component diagram)
│   └── Lab3_Alumni_Mentorship_Component_Diagram.pdf    (diagram PDF)
├── Documentation/
│   ├── Lab3_Alumni_Mentorship_Architectural_Justification.docx
│   └── Lab3_Alumni_Mentorship_Architectural_Justification.pdf
└── Analysis/
    └── Lab3_Architecture_Analysis.md
```

## How to Edit the Diagram

The `.puml` source file can be rendered using:
- [PlantUML Online Editor](https://www.plantuml.com/plantuml/uml/)
- Any IDE with PlantUML plugin (VS Code, IntelliJ)
- Python: `pip install plantuml` (render via `plantuml.PlantUML().processes_file(...)`)
- VS Code: PlantUML extension (`Alt+D` to preview)
