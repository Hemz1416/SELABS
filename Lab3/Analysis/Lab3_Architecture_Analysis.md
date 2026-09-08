# Lab 3 – Architecture Analysis

## Alumni Mentorship & Mock Interview Platform

**Student:** HEMANT RAM NELAPATI  
**SRN:** PES2UG24CS192  
**Domain:** Campus & Academic Operations  
**Actors:** Student Mentee, Alumni Mentor

---

## 1. Requirements Analysis

### 1.1 Functional Requirements

| ID   | Requirement                          | Description                                                              |
|------|--------------------------------------|--------------------------------------------------------------------------|
| FR-1 | Student Authentication               | Students register and log in using institutional credentials.            |
| FR-2 | Alumni Authentication                | Alumni register, log in, and undergo profile verification.               |
| FR-3 | Student Profile Management           | Students create/edit profiles with academic details and interests.       |
| FR-4 | Alumni Profile Management            | Alumni create/edit profiles with industry experience and expertise.      |
| FR-5 | Mentor Discovery & Search            | Students browse and search for alumni mentors by domain/skill.          |
| FR-6 | Mentorship Request & Matching        | Students send mentorship requests; alumni accept or decline.            |
| FR-7 | Mentorship Session Management        | Track ongoing mentorship sessions, session history, and notes.          |
| FR-8 | Mock Interview Scheduling            | Students book mock interview slots from alumni availability calendars.  |
| FR-9 | Interview Feedback & Evaluation      | Alumni submit structured feedback/scorecards after mock interviews.     |
| FR-10| Notifications                        | Email/in-app notifications for requests, confirmations, reminders.     |
| FR-11| Persistent Data Storage              | All user, session, and feedback data is stored reliably.               |

### 1.2 Non-Functional Requirements

| ID    | Category        | Requirement                                                                  |
|-------|-----------------|------------------------------------------------------------------------------|
| NFR-1 | Security        | Role-based access control (Student vs. Alumni vs. Admin).                   |
| NFR-2 | Security        | Encrypted credential storage and secure session tokens.                     |
| NFR-3 | Performance     | Search and scheduling responses within 2 seconds under typical load.        |
| NFR-4 | Usability       | Intuitive UI for both students and alumni with minimal training.            |
| NFR-5 | Scalability     | Support growth from hundreds to thousands of users per semester.            |
| NFR-6 | Maintainability | Modular codebase with clear layer separation for easy updates.              |
| NFR-7 | Availability    | 99% uptime during academic semester periods.                                |

### 1.3 Main Challenges

- **Authentication complexity:** Two distinct user roles (Student Mentee, Alumni Mentor) with different registration workflows and permission levels.
- **Scheduling conflicts:** Preventing double-booking of mentor availability slots across concurrent requests.
- **Data integrity:** Maintaining consistent relationships between mentorship sessions, interview bookings, and feedback records.
- **Notification reliability:** Timely delivery of session reminders and request status updates.

---

## 2. Architectural Style Comparison

### 2.1 Layered Architecture (Three-Tier)

**Structure:** Presentation Layer → Business Logic Layer → Data Access Layer. Each layer communicates only with the layer directly below it.

**Application to this platform:**
- *Presentation Layer:* Student Mentee Portal and Alumni Mentor Portal (web/mobile UIs).
- *Business Logic Layer:* Authentication & User Management, Mentorship & Mock Interview Management, Notification Service.
- *Data Layer:* Centralized database access component managing all persistent storage.

**Advantages:**
- Clear separation of concerns fits the distinct UI needs (student vs. alumni portals) and shared business logic.
- Centralized data layer simplifies maintaining referential integrity across users, sessions, and feedback.
- Well-suited for the moderate scale of a campus platform.

**Disadvantages:**
- Vertical changes (e.g., adding a new field from UI to database) require modifications across all layers.
- Performance overhead from layer-to-layer calls, though negligible at this scale.

**Security:** Centralized authentication layer acts as a single enforcement point for access control, making it easier to audit and secure.

**Performance:** In-process calls between layers avoid network overhead; database connection pooling can be managed centrally.

**Complexity:** Low to moderate — familiar pattern for development teams, straightforward to deploy as a single unit.

---

### 2.2 Microservices Architecture

**Structure:** Each functional area is an independently deployable service with its own data store, communicating via APIs or message queues.

**Application to this platform:**
- Separate services for: Authentication, User Profiles, Mentorship Matching, Interview Scheduling, Notification, each with independent databases.

**Advantages:**
- Independent scaling of high-demand services (e.g., scheduling during peak registration).
- Technology flexibility per service.

**Disadvantages:**
- Massive operational overhead for a campus-scale application — container orchestration, service discovery, distributed tracing.
- Data consistency across services requires saga patterns or eventual consistency, adding complexity for a simple mentorship workflow.
- Over-engineered for the expected user base (hundreds to low thousands).

**Security:** Each service boundary requires its own authentication/authorization, increasing the attack surface and configuration complexity.

**Performance:** Network latency between services for operations that naturally involve multiple domains (e.g., scheduling requires auth + profile + calendar).

**Complexity:** Very high — disproportionate to the scale and team size of a university project.

---

### 2.3 Client-Server Architecture

**Structure:** Thin or thick clients communicate with a monolithic server that handles all business logic and data access.

**Application to this platform:**
- Web/mobile clients send requests to a single server application that processes authentication, mentorship logic, scheduling, notifications, and database access.

**Advantages:**
- Simplest deployment model — one server application.
- All logic in one place reduces coordination overhead.

**Disadvantages:**
- No internal separation of concerns — authentication, mentorship, and notification logic are intermixed in a single codebase.
- Difficult to maintain and extend as features grow; a change to notification logic might inadvertently affect scheduling.
- Testing individual features in isolation is harder without layer boundaries.

**Security:** Single entry point is simpler to secure, but lack of internal boundaries means a vulnerability in one area could expose all functionality.

**Performance:** Efficient for small scale, but monolithic processing can become a bottleneck without internal modularity.

**Complexity:** Low initial complexity, but technical debt accumulates rapidly.

---

### 2.4 Comparison Table

| Criterion                | Layered          | Microservices    | Client-Server    |
|--------------------------|------------------|------------------|------------------|
| Separation of Concerns   | ★★★★★           | ★★★★★           | ★★☆☆☆           |
| Deployment Simplicity    | ★★★★☆           | ★★☆☆☆           | ★★★★★           |
| Scalability              | ★★★☆☆           | ★★★★★           | ★★☆☆☆           |
| Security Enforcement     | ★★★★★           | ★★★☆☆           | ★★★☆☆           |
| Performance (this scale) | ★★★★★           | ★★★☆☆           | ★★★★☆           |
| Maintainability          | ★★★★★           | ★★★★☆           | ★★☆☆☆           |
| Operational Complexity   | ★★★★☆ (Low)     | ★☆☆☆☆ (High)    | ★★★★★ (Low)     |
| **Fit for this Platform**| **★★★★★**       | **★★☆☆☆**       | **★★★☆☆**       |

---

## 3. Selected Architecture: Layered (Three-Tier)

### Justification

The **Layered Architecture** is the most appropriate choice for the Alumni Mentorship & Mock Interview Platform for the following reasons:

1. **Scenario-Specific Fit (Reason 1):** The platform has two distinct user-facing portals (Student Mentee and Alumni Mentor) that share common business logic (authentication, mentorship management, scheduling). A layered approach naturally separates the presentation concerns of each portal from the shared business rules, avoiding code duplication while maintaining clean UI boundaries.

2. **Scenario-Specific Fit (Reason 2):** Mentorship sessions and mock interviews involve tightly coupled data — a single interview booking touches user profiles, availability calendars, session records, and feedback. A centralized data layer with transactional integrity is far simpler and more reliable than distributed data stores across microservices for maintaining these relationships.

3. **Security Advantage:** The business logic layer serves as a centralized security enforcement point. All requests from both portals must pass through the Authentication & User Management component before accessing any mentorship or scheduling functionality. This single chokepoint makes it straightforward to implement and audit role-based access control (RBAC) — ensuring students cannot access alumni-only features and vice versa.

4. **Performance Advantage:** In a layered architecture, all component interactions occur within the same process (in-process method calls), eliminating the network round-trip latency that microservices would introduce. For operations like searching mentors and booking interviews — which touch authentication, business logic, and data access in sequence — this results in significantly faster response times at the moderate user scale of a campus platform.

---

## 4. Component Descriptions

### 4.1 Components (6 total)

| #  | Component                               | Layer              | Responsibility                                                      |
|----|-----------------------------------------|--------------------|---------------------------------------------------------------------|
| C1 | Student Mentee Portal                   | Presentation       | UI for students to browse mentors, request sessions, schedule mock interviews, and view feedback. |
| C2 | Alumni Mentor Portal                    | Presentation       | UI for alumni to manage availability, conduct mock interviews, and submit evaluation scorecards.  |
| C3 | Authentication & User Management        | Business Logic     | Handles registration, login, session management, role-based access control, and profile CRUD.     |
| C4 | Mentorship & Mock Interview Management  | Business Logic     | Core business logic for mentor matching, session tracking, interview scheduling, and feedback.    |
| C5 | Notification Service                    | Business Logic     | Sends email and in-app notifications for requests, confirmations, reminders, and status updates.  |
| C6 | Database Access                         | Data               | Provides CRUD operations and query capabilities over the persistent data store.                  |

### 4.2 Interfaces (6 total)

| #  | Interface               | Provided By  | Required By             | Purpose                                                   |
|----|-------------------------|-------------|-------------------------|-----------------------------------------------------------|
| I1 | IAuthentication         | C3 (Auth)   | C1 (Student), C2 (Alumni) | Login, logout, session validation, role verification.    |
| I2 | IUserProfile            | C3 (Auth)   | C1 (Student), C2 (Alumni) | Create, read, update user profile information.           |
| I3 | IMentorshipService      | C4 (MIM)    | C1 (Student), C2 (Alumni) | Search mentors, send/accept requests, manage sessions.   |
| I4 | IInterviewScheduling    | C4 (MIM)    | C1 (Student), C2 (Alumni) | Book slots, manage availability, submit feedback.        |
| I5 | INotification           | C5 (Notif)  | C4 (MIM)                 | Trigger notification dispatch for session events.        |
| I6 | IDataAccess             | C6 (DB)     | C3, C4, C5               | CRUD operations on persistent storage.                   |

---

## 5. Component Interactions

```
Student Mentee Portal ──► IAuthentication ──► Authentication & User Management
Student Mentee Portal ──► IUserProfile ──► Authentication & User Management
Student Mentee Portal ──► IMentorshipService ──► Mentorship & Mock Interview Mgmt
Student Mentee Portal ──► IInterviewScheduling ──► Mentorship & Mock Interview Mgmt

Alumni Mentor Portal ──► IAuthentication ──► Authentication & User Management
Alumni Mentor Portal ──► IUserProfile ──► Authentication & User Management
Alumni Mentor Portal ──► IMentorshipService ──► Mentorship & Mock Interview Mgmt
Alumni Mentor Portal ──► IInterviewScheduling ──► Mentorship & Mock Interview Mgmt

Mentorship & Mock Interview Mgmt ──► INotification ──► Notification Service
Mentorship & Mock Interview Mgmt ──► IDataAccess ──► Database Access

Authentication & User Management ──► IDataAccess ──► Database Access
Notification Service ──► IDataAccess ──► Database Access
```

---

## 6. Validation Checklist

- [x] At least 5 components: **6 components** identified
- [x] At least 4 interfaces: **6 interfaces** defined
- [x] Provided/required interface notation: Ball (provided) and socket (required) used in diagram
- [x] Dependencies and interactions: All component interactions documented
- [x] Architecture matches justification: Layered (Three-Tier) consistently used
- [x] No Coffee Kiosk content: All content specific to Alumni Mentorship & Mock Interview Platform
- [x] Project title correct: Alumni Mentorship & Mock Interview Platform
- [x] Student name: HEMANT RAM NELAPATI
- [x] SRN: PES2UG24CS192
- [x] Written justification ≤ 1 page

---

*Document generated for Lab 3 submission — Software Engineering, Semester 5*
