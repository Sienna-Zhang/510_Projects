# Lab 1 — Two Streamlit applications

This folder contains **two separate apps** for TECHIN 510. Each lives in its own subdirectory with its own `app.py`, `requirements.txt`, and documentation.

The assignment handout PDF sits at the same level as those folders: [`510 lab1.pdf`](510%20lab1.pdf).

| Subfolder | App |
| --------- | --- |
| [`lab1_Dorothy_Dashboard/`](lab1_Dorothy_Dashboard/) | **Purchase Request Manager** (Dorothy’s app) — procurement workflow with SQLite. |
| [`lab1_GIX Wayfinder/`](lab1_GIX%20Wayfinder/) | **GIX Campus Wayfinder** — in-memory campus resource search. |

## Run Dorothy’s app

```powershell
cd lab1_Dorothy_Dashboard
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Run Wayfinder

```powershell
cd "lab1_GIX Wayfinder"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Shared ignore rules for virtual environments and caches are in [`.gitignore`](.gitignore) at this `lab1/` level.
