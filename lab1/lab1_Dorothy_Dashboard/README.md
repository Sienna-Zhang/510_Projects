# Purchase Request Manager

A course procurement workflow application built with Streamlit, backed by SQLite. Students can sign in to submit purchase requests, and admins can approve requests, track budgets, and manage course projects.

---

## Project Overview


| Item       | Details                                                      |
| ---------- | ------------------------------------------------------------ |
| Course     | TECHIN 510 — Programming for Digital and Physical Interfaces |
| Term       | 2026 Spring                                                  |
| Tech Stack | Python 3.11+, Streamlit 1.30+, SQLite, Pandas                |
| Main File  | `lab1_Dorothy_Dashboard/app.py`                                            |
| Database   | `lab1_Dorothy_Dashboard/requests.db` (auto-created at runtime)             |
| UI Theme   | UW Purple `#4B2E83` + GIX Gold `#F2A900`                     |


---

## Features

### Student

- **Login / Registration**: Register with your email on first visit; recognized automatically on return
- **Submit Purchase Request**: Fill in supplier, item, quantity, unit price, purchase link, and notes
- **My Orders**: View request history and live status; receive alerts when status or admin notes change

### Admin (Dorothy)

- **Dashboard**: View all active requests; filter by team, status, or supplier type (Amazon / Non-Amazon); supports inline single-row editing and bulk status updates
- **Course Project Setup**: Add, edit, and delete course projects and per-team budgets
- **Budget Tracking**: View spent vs. remaining budget per team per project, with a bar chart visualization
- **Archive**: Browse all archived requests; data is never deleted

---

## Directory Structure

```
lab1/
└── lab1_Dorothy_Dashboard/
    ├── app.py               # All application logic (single file)
    ├── requirements.txt     # Python dependencies
    ├── requests.db        # SQLite database (auto-generated on first run)
    ├── README.md          # This file
    └── .streamlit/
        └── config.toml    # Streamlit theme config (UW/GIX color scheme)
```

---

## Requirements

- Python **3.11** or higher
- pip (Python package manager)

---

## Quick Start (Reproducing All Results)

### Step 1: Get the Code

Download or clone this project and make sure the directory structure is intact.

### Step 2: Create and Activate a Virtual Environment

Run the following commands inside the `lab1_Dorothy_Dashboard/` directory:

**Windows (PowerShell)**

```powershell
cd lab1_Dorothy_Dashboard
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
cd lab1_Dorothy_Dashboard
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Key dependencies:

```
streamlit>=1.30.0
pandas>=2.0.0
```

### Step 4: Launch the App

```bash
streamlit run app.py
```

Once running, the terminal will display:

```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your browser to access the app.

> **Note:** On first run, the SQLite database file `requests.db` is created automatically inside `lab1_Dorothy_Dashboard/`. No manual setup is required.

---

## Usage Guide

### Registration and Login

1. Enter your email address on the login page
2. **First-time users**: Enter a display name, select a role (Student / Admin), then click **Register & Continue**
3. **Returning users**: Click **Continue** to log straight in

> Emails ending in `@uw.edu` default to the Student role; all other domains default to Admin.

### Student Workflow

1. After logging in, select **Submit Request** from the left sidebar
2. Fill in all required fields (marked with `*`) and click **Submit Request**
3. Switch to **My Orders** to check request status and read any admin notes

### Admin Workflow

1. After logging in, select the desired page from the left sidebar
2. **Course Project Setup**: Add at least one course project and per-team budget before students can submit requests
3. **Dashboard**: Approve or update requests — edit the Status column inline, or check multiple rows and use bulk update
4. **Budget Tracking**: Monitor real-time budget usage across all teams
5. **Archive**: All archived requests are preserved here permanently

---

## Database Schema

The app uses SQLite with four tables:


| Table             | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| `users`           | User records (email, role, display name)                                 |
| `course_projects` | Course projects and per-team budgets                                     |
| `requests`        | Purchase request records (includes status and archived flag)             |
| `team_budgets`    | Legacy budget table (retained for historical data; no longer written to) |


---

## Request Status Flow

```
Submitted → Approved → Ordered → Delivered
                                        ↓
                             Refunded / Archived
```


| Status    | Description                                       |
| --------- | ------------------------------------------------- |
| Submitted | Newly submitted by a student, awaiting review     |
| Approved  | Approved by an admin                              |
| Ordered   | Purchase order placed                             |
| Delivered | Item received                                     |
| Refunded  | Purchase refunded                                 |
| Archived  | Moved to the archive; visible in the Archive page |


---

## Theme Configuration

The Streamlit theme is defined in `.streamlit/config.toml`:


| Setting                  | Value     | Description                                   |
| ------------------------ | --------- | --------------------------------------------- |
| primaryColor             | `#F2A900` | GIX Gold — buttons and interactive highlights |
| backgroundColor          | `#FFFFFF` | Main content area background                  |
| secondaryBackgroundColor | `#4B2E83` | Sidebar background (UW Purple)                |
| textColor                | `#1A1A1A` | Main content text color                       |


---

## Troubleshooting

**Q: `ModuleNotFoundError: No module named 'streamlit'` on startup**  
A: Make sure the virtual environment is activated and you have run `pip install -r requirements.txt`.

**Q: Students see "No course projects have been set up yet" when submitting**  
A: Log in as an admin first and add at least one project on the **Course Project Setup** page.

**Q: How do I reset the database?**  
A: Delete `lab1_Dorothy_Dashboard/requests.db` and restart the app. The database will be re-initialized from scratch (all data will be lost).

**Q: Running new code against an existing database**  
A: The `init_db()` function automatically detects and adds any missing columns (e.g., `submitter_email`, `admin_notes`). No manual migration is needed.

---

## Version Info

- **App Version**: v2.0
- **Python**: 3.11+
- **Streamlit**: 1.40.1 (installed in virtual environment)
- **Pandas**: 2.0.3 (installed in virtual environment)

