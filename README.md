# Endpoint File Integrity Monitor (FIM) & Anti-Tamper Console

A production-ready, modular File Integrity Monitor implemented in Python using Tkinter and SQLite. Designed for high-security environments to detect unauthorized system configuration changes, malicious file injections, or structural data deletions.

## 📁 Architecture Structure
The project strictly enforces the **Single Responsibility Principle (SRP)** by decoupling components across architectural layers:
* `main.py` - Core entrypoint launcher and orchestration wireframe.
* `core/hasher.py` - Cryptographic data mapping engine utilizing block-chunked SHA-256 signatures.
* `core/fim_engine.py` - Logical validation engine assessing state delta arrays.
* `db/db_manager.py` - Persistence layer handling relational SQLite transactional commands.
* `gui/main_window.py` - Forensic monitoring console using a split-screen layout with an embedded unified diff tracker.

## 🚀 Getting Started

### Prerequisites
* Python 3.x
* Built-in standard libraries (`tkinter`, `sqlite3`, `hashlib`, `difflib`)

### Installation & Execution
1. Clone or download this project repository.
2. Navigate to the root directory:
   ```bash
   cd project_APP
   ```
3. Execute the launcher script:
   ```bash
   python main.py
   ```

## 📊 Forensic Evaluation Matrix States
* 🟩 **Created (Green):** Identifies newly injected assets/malware.
* ⬜ **Unchanged (White):** Verifies the structural health of verified configurations.
* 🟨 **Deleted (Yellow):** Alerts on unauthorized asset wiping strategies.
* 🟥 **Modified (Red):** Flags tampered resources. Selecting a red row displays an instantaneous line-by-line syntax differential tracker (`+` additions / `-` deletions).
