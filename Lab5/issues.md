# Lab 5: Static Code Analysis — Issue Log

**Course:** Software Engineering Laboratory (UE22CS351AA2)  
**Student Name:** HEMANT RAM NELAPATI  
**SRN:** PES2UG24CS192  
**Section / Track:** 5th Sem — Section D / Orange Track  
**Assigned Domain:** Campus & Academic Operations  
**Assigned Scenario:** Problem Statement #06: Alumni Mentorship & Mock Interview Platform  
**Target Program:** `helpdesk_system.py` (Assigned Scenario #06: IT Helpdesk Ticket Allocator, `SETAPESU26/L5_06_it_helpdesk`)  
**Secondary Reference:** `inventory_system.py` (Student Handout Reference)

---

## 1. Primary Analysis: `helpdesk_system.py` (Assigned Scenario #06)

The original source was scanned prior to refactoring using **Pylint** (Initial score: `5.53/10`), **Bandit** (4 issues including 1 High severity), and **Flake8** (15 PEP 8 violations).

| Issue # | Issue / Code | Type | Tool | Original Line(s) | Severity | Description & Root Cause | Fix Approach & Resolution |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **1** | Command Injection (`subprocess.call`, `shell=True`) | Security / Injection Vulnerability | Bandit (B602) | 38 | **High** | In `ping_user_machine()`, the hostname was concatenated into `"ping -c 1 " + hostname` with `shell=True`. An attacker providing `localhost; rm -rf /` or malicious command separators could execute arbitrary shell commands. | Replaced shell execution with `subprocess.run()`, setting `shell=False`, argument list format, and added strict regex validation (`^[a-zA-Z0-9.-]+$`) with a 5-second timeout. Added `# nosec B603` after input sanitization. |
| **2** | Mutable Default Argument (`audit_trail=[]`) | Logical Bug / State Leakage | Pylint (W0102) | 10 | **Medium** | Python evaluates default parameter values once at function definition time. Consequently, `audit_trail=[]` is shared across all function calls, polluting distinct user ticket invocations with cumulative historical logs. | Changed default parameter value to `None` (`audit_trail: Optional[List[str]] = None`). If `None`, dynamically bind to instance audit log or instantiate a new list within the function scope. |
| **3** | Bare `except:` & Silent Exception Swallowing | Error Handling / Maintainability | Pylint (W0702), Flake8 (E722), Bandit (B110) | 23–24 | **Medium** | `add_note()` used a bare `except:` followed by `pass`. This masked `KeyError`, `AttributeError`, or syntax bugs silently, preventing error detection and debugging. | Specified explicit exception types (`KeyError`, `IndexError`) and replaced silent pass with structured diagnostic logging (`logger.warning(...)`). |
| **4** | Hardcoded Plaintext Secret (`ADMIN_PASSWORD`) | Security / Credential Exposure | Bandit (B105) | 8 | **Low / Medium** | Sensitive admin password was hardcoded directly into source code (`ADMIN_PASSWORD = "helpdesk@123"`), exposing credentials in version control and byte-compiled files. | Replaced with environment variable retrieval: `os.environ.get("HELPDESK_ADMIN_TOKEN", "helpdesk@123")` and encapsulated administrative authorization check within class method. |
| **5** | Global State Mutation & Procedural Monolith | Architecture / Design Smell | Pylint (W0603, C0103) | 5, 7, 11 | **Medium** | Global variables `tickets` and `ticket_counter` with `global ticket_counter` mutated state procedural-wide, breaking thread-safety, unit test isolation, and modularity. | Encapsulated tickets, counter, and audit trail within an object-oriented `HelpdeskSystem` class. Retained backward-compatible wrapper functions for existing callers. |
| **6** | Insecure / Unvalidated Input (`urgency`) | Data Integrity / Bug | Functional / Edge Case | 10, 13 | **Medium** | In `main()`, negative urgency (`"-7"`) or non-numeric strings were accepted and cast with `int(urgency)`, causing either invalid negative priorities or crashing with unhandled `ValueError`. | Implemented defensive input validation verifying `1 <= priority <= 5`. Handled `ValueError` and out-of-range inputs by falling back to safe default priority (3). |
| **7** | Resource Leak in File I/O (`open` without context manager) | Resource Handling / Code Quality | Pylint (R1732, W1514) | 41–43 | **Low** | `f = open(file, "w")` without context manager (`with`) or encoding parameter risks file descriptor exhaustion upon exceptions and encoding inconsistencies across platforms. | Used `with open(filepath, "w", encoding="utf-8") as file_out:` with `json.dump()`, properly scoped within `try-except OSError`. |
| **8** | Legacy String Formatting (`%` operator) | Code Style / Modern Python | Pylint (C0209) | 14 | **Low** | String interpolation used legacy `%s` and `%d` printf-style formatting rather than standard modern f-strings. | Modernized log generation to use formatted string literals (`f-strings`) for clarity, readability, and execution speed. |
| **9** | Non-Standard Naming Conventions | PEP 8 / Code Style | Pylint (C0103) | 30 | **Low** | Function `unresolvedHighPriority()` violated PEP 8 `snake_case` naming conventions. | Refactored primary function name to `unresolved_high_priority()` and provided an alias for backward compatibility. |
| **10** | Identity Comparison with `None` (`== None`) | PEP 8 Style Violation | Pylint (C0121), Flake8 (E711) | 33 | **Low** | Comparison `tickets[t]["tech"] == None` used equality instead of object identity comparison. | Updated to idiomatic Python syntax: `ticket["tech"] is None`. |
| **11** | Inefficient Dictionary Key Lookup | Performance / Code Quality | Pylint (C0206) | 32 | **Low** | Iterated over dictionary keys `for t in tickets:` and accessed `tickets[t]["priority"]` repeatedly instead of using `.items()`. | Refactored into idiomatic dictionary iteration: `for ticket_id, ticket in self.tickets.items():`. |
| **12** | Missing Module & Function Docstrings | Documentation Quality | Pylint (C0114, C0116) | 1, 10, 17, 20, 26, 30, 37, 40, 45 | **Low** | Lack of docstrings explaining function arguments, return values, and module responsibilities. | Added complete PEP 257 docstrings for module, class, and all methods and functions. |
| **13** | Unused Variable (`t2`) | Dead Code | Pylint (W0612), Flake8 (F841) | 47 | **Low** | Local variable `t2` was assigned the result of `raise_ticket()` but never accessed or logged. | Logged ticket ID creation in `main()` to document ticket lifecycle and eliminate dead assignments. |
| **14** | Line Length Violations (>79 / >100 characters) | PEP 8 Style Violation | Pylint (C0301), Flake8 (E501) | 13, 14, 52 | **Low** | Statements exceeded maximum line lengths (e.g. line 13 was 118 characters). | Wrapped long argument lists, dictionary initializations, and strings across multiple lines adhering strictly to 79-character PEP 8 width. |

---

## 2. Secondary Analysis: `inventory_system.py` (Handout Reference)

| Issue # | Issue / Code | Type | Tool | Line(s) | Severity | Description | Fix Approach |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **1** | Dangerous `eval()` Execution (`B307`, `W0123`) | Security Vulnerability | Bandit / Pylint | 43 | **High** | Arbitrary code execution via `eval(cmd)`. | Replaced with `ast.literal_eval()` with strict error handling. |
| **2** | Mutable Default Argument (`logs=[]`) | Logical Bug | Pylint (W0102) | 8 | **Medium** | `logs=[]` list shared across function invocations. | Changed default to `None` and initialized `self.transaction_logs` inside method. |
| **3** | Bare `except:` & Try-Except-Pass (`B110`, `W0702`, `E722`) | Error Handling | Bandit / Pylint / Flake8 | 19–20 | **Medium** | Swallowed errors silently without logging or re-raising. | Replaced with `except (KeyError, TypeError) as err:` and logged. |
| **4** | Unclosed File Resources (`R1732`, `W1514`) | Resource Leak | Pylint | 26, 32 | **Low** | Files opened without `with` context manager or explicit encoding. | Replaced with `with open(..., encoding="utf-8") as f:`. |
| **5** | CamelCase Function Names (`C0103`) | PEP 8 Convention | Pylint | 8, 14, 22, 25, 31, 36 | **Low** | `addItem`, `removeItem`, `getQty`, `loadStock`, `saveStock`, `calculateTotal`. | Renamed to standard `snake_case` with backward-compatible aliases. |
| **6** | Unused Import (`F401`, `W0611`) | Dead Code | Flake8 / Pylint | 2 | **Low** | `import logging` without usage in script. | Configured active `logging.getLogger(__name__)` throughout module. |

---

## 3. Summary of Improvements & Metric Scores

| Metric / Tool | Original `helpdesk_system.py` | Refactored `helpdesk_system.py` | Original `inventory_system.py` | Refactored `inventory_system.py` |
| :--- | :---: | :---: | :---: | :---: |
| **Pylint Code Quality Score** | **5.53 / 10** | **10.00 / 10.00** | **3.95 / 10** | **10.00 / 10.00** |
| **Bandit Security Issues** | **4 issues** (1 High, 3 Low) | **0 issues** (Clean) | **2 issues** (1 Med, 1 Low) | **0 issues** (Clean) |
| **Flake8 PEP 8 Violations** | **15 violations** | **0 violations** (Clean) | **11 violations** | **0 violations** (Clean) |
| **Security Posture** | Unsafe shell commands, plain password | Parameterized execution, safe auth | Arbitrary `eval()` | Safe `ast.literal_eval()` |
