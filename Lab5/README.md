# Lab 5: Static Code Analysis (Pylint, Bandit, Flake8)
**UE22CS351AA2: Software Engineering Laboratory — 5th Semester**  
**Department of Computer Science and Engineering — PES University**

| Student Information | Details |
| :--- | :--- |
| **Student Name** | HEMANT RAM NELAPATI |
| **SRN** | PES2UG24CS192 |
| **Section / Track** | 5th Sem — Section D / Orange Track |
| **Assigned Domain** | Campus & Academic Operations |
| **Assigned Scenario** | Problem Statement #06: Alumni Mentorship & Mock Interview Platform |
| **Target Program** | `helpdesk_system.py` (Assigned Scenario #06: IT Helpdesk Ticket Allocator) |
| **Secondary Reference** | `inventory_system.py` (Student Handout Reference) |
| **Pylint Score** | **10.00 / 10.00 (Perfect Score — 0 Issues)** |
| **Bandit Score** | **0 Vulnerabilities (0 High, 0 Medium, 0 Low)** |
| **Flake8 Score** | **0 Style Violations (Clean PEP 8 Compliance)** |

---

## 1. Overview & Objectives
Static code analysis systematically inspects source code without execution to identify bugs, architectural anti-patterns, security vulnerabilities, and code style violations. This lab utilizes three industry-standard tools:
- **Pylint:** Deep code quality analysis, logical errors, design flaws, and convention adherence.
- **Bandit:** Automated AST-based security vulnerability scanner for Python.
- **Flake8:** PEP 8 compliance, formatting, whitespace, line length, and syntax linter.

---

## 2. Deliverables & Repository Structure

```
SELABS/Lab5/
├── PES2UG24CS192_Lab5.pdf                    # Official Submission Report (PDF)
├── README.md                                 # Laboratory Overview & Execution Guide
├── helpdesk_system.py                        # Refactored Assigned Scenario #06 Script (10.00/10)
├── original_helpdesk_system.py               # Original Starter Script for Problem Statement #06
├── inventory_system.py                       # Refactored Handout Reference Script (10.00/10)
├── original_inventory_system.py              # Original Handout Reference Starter Script
├── issues.md                                 # Comprehensive Prioritized Issue Log
├── reflection.md                             # Answers to Reflection Questions 1 through 4
├── pylint_report.txt                         # Pylint Verification Report (10.00/10)
├── bandit_report.txt                         # Bandit Verification Report (0 issues)
├── flake8_report.txt                         # Flake8 Verification Report (0 errors)
├── initial_pylint_report.txt                 # Baseline Pylint Report (5.53/10)
├── initial_bandit_report.txt                 # Baseline Bandit Report (4 issues)
├── initial_flake8_report.txt                 # Baseline Flake8 Report (15 violations)
├── inventory_pylint_report.txt               # Handout Script Pylint Report (10.00/10)
├── inventory_bandit_report.txt               # Handout Script Bandit Report (0 issues)
├── inventory_flake8_report.txt               # Handout Script Flake8 Report (0 errors)
├── generate_lab5_pdf.py                      # ReportLab PDF Generator Script
└── Lab_5_Static_Code_Analysis_Student_handout.docx # Student Handout
```

---

## 3. Comparative Metric Scores

| Target Program | Static Analysis Tool | Original Baseline | Refactored Version | Result / Status |
| :--- | :--- | :---: | :---: | :--- |
| **helpdesk_system.py**<br/>*(Assigned Scenario #06)* | **Pylint**<br/>**Bandit**<br/>**Flake8** | 5.53 / 10<br/>4 issues (1 High, 3 Low)<br/>15 PEP 8 violations | **10.00 / 10.00**<br/>**0 issues**<br/>**0 violations** | **+4.47 Score Increase**<br/>All RCE & passwords fixed<br/>Zero PEP 8 style errors |
| **inventory_system.py**<br/>*(Handout Reference)* | **Pylint**<br/>**Bandit**<br/>**Flake8** | 3.95 / 10<br/>2 issues (1 Med, 1 Low)<br/>11 PEP 8 violations | **10.00 / 10.00**<br/>**0 issues**<br/>**0 violations** | **+6.05 Score Increase**<br/>`eval()` eliminated with `ast.literal_eval`<br/>Safe UTF-8 context managers |

---

## 4. Key Fixes Applied

1. **Remote Command Injection (Bandit B602 - High Severity):**
   - Replaced vulnerable shell concatenation `subprocess.call("ping -c 1 " + hostname, shell=True)` with safe argument lists `subprocess.run(["ping", "-n", "1", clean_host], shell=False, timeout=5)`.
   - Implemented strict regex whitelist verification (`^[a-zA-Z0-9.-]+$`).
2. **Mutable Default Argument Bug (Pylint W0102 - Medium Severity):**
   - Redefined default argument from mutable list `audit_trail=[]` to `audit_trail: Optional[List[str]] = None`, dynamically instantiating within function scope to eliminate cross-ticket data leaks.
3. **Bare Exception Handling & Swallowed Errors (Pylint W0702, Bandit B110, Flake8 E722):**
   - Eliminated blind `try...except: pass` in favor of targeted `KeyError` and `ValueError` handlers coupled with structured diagnostic logging via `logging.getLogger(__name__)`.
4. **Plaintext Credential Exposure (Bandit B105 - Medium Severity):**
   - Removed hardcoded plaintext administrator password `helpdesk@123`. Retrieved token securely from environment variables (`os.environ.get("HELPDESK_ADMIN_TOKEN")`).
5. **Procedural Global State to Object-Oriented Architecture (Pylint W0603, C0103):**
   - Encapsulated ticket storage, ID tracking, and audit trails within a cohesive `HelpdeskSystem` class. Provided backward-compatible module wrapper functions.

---

## 5. Verification Commands

To reproduce and verify the static analysis reports locally:

```bash
# 1. Run Pylint (Verifies 10.00/10 score)
python -m pylint helpdesk_system.py

# 2. Run Bandit (Verifies 0 security vulnerabilities)
python -m bandit -r helpdesk_system.py

# 3. Run Flake8 (Verifies 0 PEP 8 errors)
python -m flake8 helpdesk_system.py

# 4. Execute the script to test runtime behavior
python helpdesk_system.py
```
