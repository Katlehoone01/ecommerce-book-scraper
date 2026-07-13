# Autonomous Multi-Page E-Commerce Web Scraper

A multi-variant Python data harvesting pipeline designed to parse paginated web architectures, execute structural data transformations, and stream outputs into both flat-file and relational database architectures.

## 🚀 Key Features

* **Pagination Loop Engine**: Sequentially traverses dynamic web pagination rules across multi-page layouts without human intervention.
* **Dual-Target Storage Architectures**:
  * **Flat-File Pipeline (`scraper.py`)**: Normalizes raw data text strings into a structured, permanent CSV spreadsheet ledger.
  * **Relational Database Pipeline (`scraper_to_sql.py`)**: Normalizes and cleans raw currency strings into strict `REAL` float attributes, feeding directly into a localized SQLite3 relational database schema.
* **Autonomous Task Scheduling**: Packaged via Windows Batch scripting (`.bat`) to execute seamlessly overnight via local OS task managers.
* **Production Error Logging**: Implements localized status monitoring that records time-stamped successes or trace exceptions directly to a permanent tracking log.

## 🛠️ Tech Stack & Dependencies

* **Language**: Python 3
* **SQL Engine**: SQLite3 (Native relational core)
* **Libraries**: BeautifulSoup4, Requests, CSV, Datetime, OS
* **Deployment**: Windows Batch Scripting, Windows Task Scheduler

## 📁 Repository Structure

* `scraper.py` - Core execution engine outputting to a CSV spreadsheet.
* `scraper_to_sql.py` - Advanced pipeline engine featuring SQLite data streaming integrations.
* `run_pipeline.bat` - Automation shell script handling OS task triggers.
* `.gitignore` - Enforced environment security masks ignoring local system binaries, logs, and database artifacts.
