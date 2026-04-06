# This Streamlit app is Purchase Request Manager — a course procurement workflow backed by SQLite.
# Students sign in, submit purchase requests against course projects, and review their orders.
# Admins configure projects/budgets, work the request dashboard, track team spending, and browse archives.
# I manually changed the sidebar radio label from "Navigation" to "Pages".

from __future__ import annotations

import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────

DB_PATH = Path(__file__).parent / "requests.db"

STATUSES = ["Submitted", "Approved", "Ordered", "Delivered", "Refunded", "Archived"]


# ─────────────────────────────────────────────
# Database helpers — schema
# ─────────────────────────────────────────────

# Initialise the SQLite database; creates all tables if they do not exist yet,
# and adds any missing columns to existing tables (safe to run on old DBs)
def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        # Users table: stores email, role, and display name
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email        TEXT PRIMARY KEY,
                role         TEXT NOT NULL CHECK(role IN ('student','admin')),
                display_name TEXT NOT NULL DEFAULT ''
            )
        """)

        # Course projects table: Dorothy sets these up in advance
        conn.execute("""
            CREATE TABLE IF NOT EXISTS course_projects (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                name   TEXT NOT NULL,
                budget REAL NOT NULL DEFAULT 0
            )
        """)

        # Requests table (legacy + new columns)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                team             INTEGER NOT NULL DEFAULT 0,
                cfo_name         TEXT    NOT NULL,
                course           TEXT    NOT NULL,
                supplier         TEXT    NOT NULL,
                item_name        TEXT    NOT NULL,
                quantity         INTEGER NOT NULL,
                unit_price       REAL    NOT NULL,
                total_price      REAL    NOT NULL,
                purchase_link    TEXT    NOT NULL,
                notes            TEXT    DEFAULT '',
                admin_notes      TEXT    DEFAULT '',
                request_status   TEXT    NOT NULL DEFAULT 'Submitted',
                archived         INTEGER NOT NULL DEFAULT 0,
                created_at       TEXT    NOT NULL,
                updated_at       TEXT    NOT NULL,
                submitter_email  TEXT    NOT NULL DEFAULT ''
            )
        """)

        # Legacy budget table — kept for historical data, no longer written
        conn.execute("""
            CREATE TABLE IF NOT EXISTS team_budgets (
                team    INTEGER PRIMARY KEY,
                budget  REAL    NOT NULL DEFAULT 0
            )
        """)

        # Safely add submitter_email column to old DBs that predate this schema
        existing_cols = [
            row[1] for row in conn.execute("PRAGMA table_info(requests)").fetchall()
        ]
        if "submitter_email" not in existing_cols:
            conn.execute(
                "ALTER TABLE requests ADD COLUMN submitter_email TEXT NOT NULL DEFAULT ''"
            )
        if "admin_notes" not in existing_cols:
            conn.execute(
                "ALTER TABLE requests ADD COLUMN admin_notes TEXT DEFAULT ''"
            )

        conn.commit()


# ─────────────────────────────────────────────
# Database helpers — users
# ─────────────────────────────────────────────

# Look up a user by email; returns a dict with keys email/role/display_name or None
def get_user(email: str) -> dict | None:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT email, role, display_name FROM users WHERE email = ?",
            (email.lower().strip(),),
        ).fetchone()
    if row:
        return {"email": row[0], "role": row[1], "display_name": row[2]}
    return None


# Insert or update a user record in the database
def save_user(email: str, role: str, display_name: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO users (email, role, display_name) VALUES (?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET role = excluded.role,
                                             display_name = excluded.display_name
            """,
            (email.lower().strip(), role, display_name.strip()),
        )
        conn.commit()


# ─────────────────────────────────────────────
# Database helpers — course projects
# ─────────────────────────────────────────────

# Return all course projects as a DataFrame with columns id, name, budget
def get_course_projects() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT id, name, budget FROM course_projects ORDER BY name", conn
        )
    return df


# Insert a new course project and return its new id
def add_course_project(name: str, budget: float) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO course_projects (name, budget) VALUES (?, ?)",
            (name.strip(), budget),
        )
        conn.commit()
        return cursor.lastrowid


# Update an existing course project's name and budget
def update_course_project(project_id: int, name: str, budget: float) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE course_projects SET name = ?, budget = ? WHERE id = ?",
            (name.strip(), budget, project_id),
        )
        conn.commit()


# Delete a course project by id
def delete_course_project(project_id: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM course_projects WHERE id = ?", (project_id,))
        conn.commit()


# ─────────────────────────────────────────────
# Database helpers — requests
# ─────────────────────────────────────────────

# Insert a new purchase request into the database and return the new row id
def submit_request(
    team: int,
    cfo_name: str,
    course: str,
    supplier: str,
    item_name: str,
    quantity: int,
    unit_price: float,
    total_price: float,
    purchase_link: str,
    notes: str,
    submitter_email: str,
) -> int:
    now = datetime.now().isoformat(sep=" ", timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO requests
                (team, cfo_name, course, supplier, item_name, quantity,
                 unit_price, total_price, purchase_link, notes,
                 request_status, archived, created_at, updated_at, submitter_email)
            VALUES (?,?,?,?,?,?,?,?,?,?,'Submitted',0,?,?,?)
            """,
            (team, cfo_name, course, supplier, item_name, quantity,
             unit_price, total_price, purchase_link, notes, now, now, submitter_email),
        )
        conn.commit()
        return cursor.lastrowid


# Fetch all non-archived requests as a DataFrame
def get_all_requests() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM requests WHERE archived = 0 ORDER BY created_at DESC",
            conn,
        )
    return df


# Fetch only archived requests as a DataFrame
def get_archived_requests() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM requests WHERE archived = 1 ORDER BY updated_at DESC",
            conn,
        )
    return df


# Fetch all non-archived requests submitted by a specific email address
def get_my_requests(email: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            """
            SELECT id, team, cfo_name, course, supplier, item_name,
                   quantity, unit_price, total_price, request_status,
                   purchase_link, notes, admin_notes, created_at, updated_at
              FROM requests
             WHERE submitter_email = ?
             ORDER BY created_at DESC
            """,
            conn,
            params=(email.lower().strip(),),
        )
    return df


# Update status and optional admin notes of a request in one write operation
def update_status_and_admin_notes(
    request_id: int,
    new_status: str,
    admin_notes: str | None = None,
) -> None:
    now = datetime.now().isoformat(sep=" ", timespec="seconds")
    archived_flag = 1 if new_status == "Archived" else 0
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            UPDATE requests
               SET request_status = ?,
                   admin_notes    = CASE
                                        WHEN ? IS NULL THEN admin_notes
                                        ELSE ?
                                    END,
                   archived       = ?,
                   updated_at     = ?
             WHERE id = ?
            """,
            (
                new_status,
                admin_notes,
                admin_notes.strip() if admin_notes is not None else None,
                archived_flag,
                now,
                request_id,
            ),
        )
        conn.commit()


# Update status and optional admin notes for multiple requests in one transaction
def update_status_and_admin_notes_bulk(
    request_ids: list[int],
    new_status: str,
    admin_notes: str | None = None,
) -> None:
    if not request_ids:
        return
    now = datetime.now().isoformat(sep=" ", timespec="seconds")
    archived_flag = 1 if new_status == "Archived" else 0
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """
            UPDATE requests
               SET request_status = ?,
                   admin_notes    = CASE
                                        WHEN ? IS NULL THEN admin_notes
                                        ELSE ?
                                    END,
                   archived       = ?,
                   updated_at     = ?
             WHERE id = ?
            """,
            [
                (
                    new_status,
                    admin_notes,
                    admin_notes.strip() if admin_notes is not None else None,
                    archived_flag,
                    now,
                    rid,
                )
                for rid in request_ids
            ],
        )
        conn.commit()


# Update the status of a single request; if status is Archived also set archived flag
def update_status(request_id: int, new_status: str) -> None:
    update_status_and_admin_notes(request_id, new_status, None)


# Update the status of multiple requests in a single transaction
def update_status_bulk(request_ids: list[int], new_status: str) -> None:
    update_status_and_admin_notes_bulk(request_ids, new_status, None)


# Classify a request as 'Amazon' or 'Non-Amazon' based on supplier name or purchase link
def classify_amazon(supplier: str, link: str) -> str:
    if "amazon" in supplier.lower() or "amazon.com" in link.lower():
        return "Amazon"
    return "Non-Amazon"


# ─────────────────────────────────────────────
# Database helpers — budget
# ─────────────────────────────────────────────

# Return per-team spending vs per-team budget as a DataFrame.
# Each row represents one (course project, team) pair.
# The budget column in course_projects represents the budget allocated to EACH team.
def get_budget_by_team() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        # Per-team budget from course_projects (keyed on project name)
        projects = pd.read_sql_query(
            "SELECT name, budget AS per_team_budget FROM course_projects", conn
        )
        # Aggregate spending per (course project, team) across non-refunded active requests
        spending = pd.read_sql_query(
            """
            SELECT course, team, SUM(total_price) AS spent
              FROM requests
             WHERE request_status != 'Refunded'
               AND archived = 0
             GROUP BY course, team
            """,
            conn,
        )

    if spending.empty:
        return pd.DataFrame(
            columns=["Project", "Team", "Per-Team Budget ($)", "Spent ($)", "Remaining ($)"]
        )

    # Join per-team budget onto each (course, team) spending row
    summary = spending.merge(projects, left_on="course", right_on="name", how="left")
    summary["per_team_budget"] = summary["per_team_budget"].fillna(0.0)
    summary["remaining"] = summary["per_team_budget"] - summary["spent"]
    summary = summary.rename(
        columns={
            "course": "Project",
            "team": "Team",
            "per_team_budget": "Per-Team Budget ($)",
            "spent": "Spent ($)",
            "remaining": "Remaining ($)",
        }
    )
    summary = summary.sort_values(["Project", "Team"])
    return summary[["Project", "Team", "Per-Team Budget ($)", "Spent ($)", "Remaining ($)"]]


# ─────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────

# Validate the student submission form fields; return a list of error strings
def validate_form(
    team: int | None,
    cfo_name: str,
    course: str,
    supplier: str,
    item_name: str,
    quantity: int | None,
    unit_price: float | None,
    purchase_link: str,
) -> list[str]:
    errors: list[str] = []
    if team is None or team <= 0:
        errors.append("Team number must be a positive integer.")
    if not cfo_name.strip():
        errors.append("CFO name is required.")
    if not course.strip():
        errors.append("Please select a course project.")
    if not supplier.strip():
        errors.append("Supplier is required.")
    if not item_name.strip():
        errors.append("Item name is required.")
    if quantity is None or quantity <= 0:
        errors.append("Quantity must be a positive integer.")
    if unit_price is None or unit_price <= 0:
        errors.append("Unit price must be greater than zero.")
    if not purchase_link.strip():
        errors.append("Purchase link is required.")
    elif not purchase_link.strip().startswith("http"):
        errors.append("Purchase link must start with http:// or https://.")
    return errors


# ─────────────────────────────────────────────
# Page renderers — auth
# ─────────────────────────────────────────────

# Render the login / registration page and manage session_state["user"]
def page_login() -> None:
    st.title("Purchase Request Manager")
    st.write("Please enter your email address to continue.")

    email = st.text_input("Email address", placeholder="yourname@uw.edu").strip().lower()

    if not email:
        return

    if not ("@" in email and "." in email.split("@")[-1]):
        st.error("Please enter a valid email address.")
        return

    existing = get_user(email)

    if existing:
        # Known user — log them straight in
        st.success(f"Welcome back, **{existing['display_name'] or email}**!")
        if st.button("Continue", type="primary"):
            st.session_state["user"] = existing
            st.rerun()
    else:
        # New user — ask for display name and role
        st.info("First time here! Please complete your profile.")
        display_name = st.text_input("Your display name", placeholder="Full name")

        # Default suggestion based on email domain
        default_role = "Student" if email.endswith("@uw.edu") else "Admin"
        role_label = st.radio(
            "I am a ...",
            ["Student", "Admin"],
            index=0 if default_role == "Student" else 1,
        )
        role = "student" if role_label == "Student" else "admin"

        if st.button("Register & Continue", type="primary"):
            if not display_name.strip():
                st.error("Display name is required.")
            else:
                save_user(email, role, display_name)
                user = get_user(email)
                st.session_state["user"] = user
                st.rerun()


# ─────────────────────────────────────────────
# Page renderers — student
# ─────────────────────────────────────────────

# Render the student purchase request submission form
def page_submission_form() -> None:
    user = st.session_state["user"]
    st.title("Submit a Purchase Request")
    st.write("Fill in all required fields below. Fields marked with * are required.")

    # Load course projects for the dropdown
    projects_df = get_course_projects()
    if projects_df.empty:
        st.warning(
            "No course projects have been set up yet. "
            "Please ask your instructor to add one before submitting."
        )
        return

    project_options = projects_df["name"].tolist()

    with st.form("submission_form", clear_on_submit=True):
        # Submitter info (read-only display)
        st.info(f"Submitting as: **{user['email']}**")

        col1, col2 = st.columns(2)

        with col1:
            course = st.selectbox("Course Project *", project_options)
            team = st.number_input(
                "Team Number *", min_value=1, step=1, value=None, placeholder="e.g. 3"
            )
            cfo_name = st.text_input(
                "CFO Name *",
                value=user.get("display_name", ""),
                placeholder="Full name",
            )
            supplier = st.text_input(
                "Supplier *", placeholder="e.g. Amazon, Home Depot"
            )
            item_name = st.text_input(
                "Item Name *", placeholder="e.g. Arduino Uno Rev3"
            )

        with col2:
            quantity = st.number_input(
                "Quantity *", min_value=1, step=1, value=None, placeholder="e.g. 2"
            )
            unit_price = st.number_input(
                "Unit Price ($) *",
                min_value=0.01,
                step=0.01,
                value=None,
                placeholder="e.g. 25.99",
            )

            if quantity and unit_price:
                total_price = round(float(quantity) * float(unit_price), 2)
                st.metric("Total Price ($)", f"{total_price:.2f}")
            else:
                total_price = 0.0
                st.metric("Total Price ($)", "—")

            purchase_link = st.text_input("Purchase Link *", placeholder="https://...")
            notes = st.text_area(
                "Notes (optional)", placeholder="Any additional details..."
            )

        submitted = st.form_submit_button("Submit Request", use_container_width=True)

    if submitted:
        q = int(quantity) if quantity else None
        up = float(unit_price) if unit_price else None
        total_price = round(q * up, 2) if (q and up) else 0.0

        errors = validate_form(
            team=int(team) if team else None,
            cfo_name=cfo_name,
            course=course,
            supplier=supplier,
            item_name=item_name,
            quantity=q,
            unit_price=up,
            purchase_link=purchase_link,
        )

        if errors:
            st.error("Please fix the following errors before submitting:")
            for err in errors:
                st.write(f"- {err}")
        else:
            new_id = submit_request(
                team=int(team),
                cfo_name=cfo_name.strip(),
                course=course,
                supplier=supplier.strip(),
                item_name=item_name.strip(),
                quantity=q,
                unit_price=up,
                total_price=total_price,
                purchase_link=purchase_link.strip(),
                notes=notes.strip(),
                submitter_email=user["email"],
            )
            st.success(f"Request #{new_id} submitted successfully!")
            st.write("**Submission Summary**")
            summary_data = {
                "Field": [
                    "Request ID", "Submitter", "Team", "CFO", "Course Project",
                    "Supplier", "Item", "Qty", "Unit Price", "Total Price",
                    "Link", "Notes",
                ],
                "Value": [
                    new_id, user["email"], int(team), cfo_name, course,
                    supplier, item_name, q, f"${up:.2f}", f"${total_price:.2f}",
                    purchase_link, notes or "—",
                ],
            }
            st.table(pd.DataFrame(summary_data))


# Render the student's own order history with live status
def page_my_orders() -> None:
    user = st.session_state["user"]
    st.title("My Orders")
    st.write(f"Showing all purchase requests submitted by **{user['email']}**.")

    df = get_my_requests(user["email"])

    if df.empty:
        st.info("You haven't submitted any requests yet.")
        return

    # Track a per-user "seen snapshot" so only status/admin-note changes trigger alerts.
    seen_key = "student_order_seen_snapshot"
    all_seen = st.session_state.get(seen_key, {})
    if not isinstance(all_seen, dict):
        all_seen = {}
    email_key = user["email"].lower().strip()
    user_seen = all_seen.get(email_key, {})
    if not isinstance(user_seen, dict):
        user_seen = {}

    row_signatures: dict[str, dict[str, str]] = {}
    unread_ids: list[str] = []
    for _, row in df.iterrows():
        rid = str(int(row["id"]))
        signature = {
            "request_status": str(row["request_status"]),
            "admin_notes": str(row["admin_notes"] or ""),
        }
        row_signatures[rid] = signature
        previous_signature = user_seen.get(rid)
        if previous_signature is None:
            # First time this user sees this request: initialise as read.
            user_seen[rid] = signature
        elif previous_signature != signature:
            unread_ids.append(rid)

    all_seen[email_key] = {
        rid: user_seen.get(rid, signature)
        for rid, signature in row_signatures.items()
    }
    st.session_state[seen_key] = all_seen

    unread_count = len(unread_ids)
    if unread_count > 0:
        st.warning(f"You have {unread_count} request update(s): status or admin notes changed.")
        if st.button("Mark all updates as read", key="mark_updates_read"):
            all_seen[email_key] = row_signatures
            st.session_state[seen_key] = all_seen
            st.success("All request updates have been marked as read.")
            st.rerun()

    unread_set = set(unread_ids)
    status_color = {
        "Submitted": "🔵",
        "Approved": "🟢",
        "Ordered": "🟡",
        "Delivered": "✅",
        "Refunded": "🔴",
        "Archived": "⚫",
    }

    for _, row in df.iterrows():
        rid = str(int(row["id"]))
        update_badge = " 🆕" if rid in unread_set else ""
        icon = status_color.get(row["request_status"], "⬜")
        with st.expander(
            f"{icon} #{row['id']} — {row['item_name']} | {row['request_status']}{update_badge}",
            expanded=False,
        ):
            c1, c2 = st.columns(2)
            c1.write(f"**Course Project:** {row['course']}")
            c1.write(f"**Team:** {row['team']}")
            c1.write(f"**Supplier:** {row['supplier']}")
            c1.write(f"**Item:** {row['item_name']}")
            c1.write(f"**Qty:** {row['quantity']}  |  **Unit Price:** ${row['unit_price']:.2f}")
            c1.write(f"**Total:** ${row['total_price']:.2f}")
            c2.write(f"**Status:** {row['request_status']}")
            c2.write(f"**Submitted:** {row['created_at']}")
            c2.write(f"**Last Updated:** {row['updated_at']}")
            if row["purchase_link"]:
                c2.markdown(f"[Purchase Link]({row['purchase_link']})")
            if row["notes"]:
                st.write(f"**Your Notes:** {row['notes']}")
            if row["admin_notes"]:
                st.info(f"**Admin Notes:** {row['admin_notes']}")


# ─────────────────────────────────────────────
# Page renderers — admin
# ─────────────────────────────────────────────

# Render Dorothy's management dashboard: view and update all active requests
def page_dashboard() -> None:
    st.title("Dorothy's Dashboard")
    st.write("View, filter, and update the status of all active purchase requests.")

    df = get_all_requests()

    if df.empty:
        st.info("No active requests yet.")
        return

    # Add Amazon/Non-Amazon classification column
    df["amazon_type"] = df.apply(
        lambda r: classify_amazon(str(r["supplier"]), str(r["purchase_link"])), axis=1
    )

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        team_options = ["All"] + sorted(df["team"].unique().tolist())
        selected_team = st.selectbox("Filter by Team", team_options)

    with col_f2:
        status_options = ["All"] + STATUSES
        selected_status = st.selectbox("Filter by Status", status_options)

    with col_f3:
        supplier_type_options = ["All", "Amazon", "Non-Amazon"]
        selected_supplier_type = st.selectbox("Filter by Supplier Type", supplier_type_options)

    with col_f4:
        sort_order = st.selectbox("Sort by Date", ["Newest first", "Oldest first"])

    filtered = df.copy()
    if selected_team != "All":
        filtered = filtered[filtered["team"] == int(selected_team)]
    if selected_status != "All":
        filtered = filtered[filtered["request_status"] == selected_status]
    if selected_supplier_type != "All":
        filtered = filtered[filtered["amazon_type"] == selected_supplier_type]

    ascending = sort_order == "Oldest first"
    filtered = filtered.sort_values("created_at", ascending=ascending).reset_index(drop=True)
    if "admin_notes" not in filtered.columns:
        filtered["admin_notes"] = ""
    else:
        filtered["admin_notes"] = filtered["admin_notes"].fillna("")

    st.write(f"Showing **{len(filtered)}** request(s)")

    if filtered.empty:
        st.info("No requests match the current filters.")
        return

    # Build the editor dataframe: add a Select checkbox column at the front
    editor_cols = [
        "id", "submitter_email", "team", "cfo_name", "course", "supplier",
        "amazon_type", "item_name", "quantity", "unit_price", "total_price",
        "request_status", "admin_notes", "created_at", "updated_at",
    ]
    editor_cols = [c for c in editor_cols if c in filtered.columns]
    editor_df = filtered[editor_cols].copy()
    editor_df.insert(0, "Select", False)

    edited = st.data_editor(
        editor_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", help="Tick to bulk-update", default=False),
            "request_status": st.column_config.SelectboxColumn(
                "Status",
                options=STATUSES,
                required=True,
                help="Change status directly here",
            ),
            "admin_notes": st.column_config.TextColumn(
                "Admin Notes",
                help="Visible to students (e.g., reason for not approving).",
            ),
            "amazon_type": st.column_config.TextColumn("Supplier Type", disabled=True),
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "submitter_email": st.column_config.TextColumn("Submitter", disabled=True),
            "team": st.column_config.NumberColumn("Team", disabled=True),
            "cfo_name": st.column_config.TextColumn("CFO", disabled=True),
            "course": st.column_config.TextColumn("Course", disabled=True),
            "supplier": st.column_config.TextColumn("Supplier", disabled=True),
            "item_name": st.column_config.TextColumn("Item", disabled=True),
            "quantity": st.column_config.NumberColumn("Qty", disabled=True),
            "unit_price": st.column_config.NumberColumn("Unit Price ($)", disabled=True),
            "total_price": st.column_config.NumberColumn("Total ($)", disabled=True),
            "created_at": st.column_config.TextColumn("Submitted", disabled=True),
            "updated_at": st.column_config.TextColumn("Updated", disabled=True),
        },
        key="dashboard_editor",
    )

    # Handle inline per-row status changes via the data_editor diff
    if edited is not None:
        for row_idx, changes in st.session_state.get("dashboard_editor", {}).get("edited_rows", {}).items():
            if "request_status" in changes or "admin_notes" in changes:
                row_id = int(editor_df.iloc[row_idx]["id"])
                current_status = str(editor_df.iloc[row_idx]["request_status"])
                current_admin_notes = str(editor_df.iloc[row_idx]["admin_notes"] or "")
                new_status = str(changes.get("request_status", current_status))
                new_admin_notes = str(changes.get("admin_notes", current_admin_notes))
                update_status_and_admin_notes(row_id, new_status, new_admin_notes)
                st.success(f"Request #{row_id} updated (status/notes saved).")
                st.rerun()

    # Bulk status update section
    st.divider()
    st.subheader("Bulk Status Update")
    st.caption("Tick the **Select** checkboxes in the table above, then choose a target status and click Apply.")

    bulk_col1, bulk_col2 = st.columns([2, 1])
    with bulk_col1:
        bulk_status = st.selectbox("Target Status for Selected Rows", STATUSES, key="bulk_status")
        bulk_admin_notes = st.text_area(
            "Admin Notes for Selected Rows (optional)",
            placeholder="Add a shared message for selected requests...",
            key="bulk_admin_notes",
        )
    with bulk_col2:
        st.write("")  # vertical alignment spacer
        st.write("")
        apply_bulk = st.button("Apply to Selected", type="primary", use_container_width=True)

    if apply_bulk:
        selected_rows = edited[edited["Select"] == True]
        if selected_rows.empty:
            st.warning("No rows selected. Tick the Select checkbox for the rows you want to update.")
        else:
            ids_to_update = selected_rows["id"].astype(int).tolist()
            note_value = bulk_admin_notes.strip()
            update_status_and_admin_notes_bulk(
                ids_to_update,
                bulk_status,
                note_value if note_value else None,
            )
            st.success(
                f"Updated **{len(ids_to_update)}** request(s) to **{bulk_status}**: "
                + ", ".join(f"#{i}" for i in ids_to_update)
            )
            st.rerun()


# Render the course project setup page where admins manage projects and budgets
def page_course_project_setup() -> None:
    st.title("Course Project Setup")
    st.write(
        "Add or edit course projects. Students will choose from these when submitting requests."
    )

    # ── Add new project ────────────────────────────────────────────────────
    with st.expander("Add New Course Project", expanded=True):
        with st.form("add_project_form", clear_on_submit=True):
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                new_name = st.text_input("Project Name *", placeholder="e.g. INFO 510 Spring 2026")
            with p_col2:
                new_budget = st.number_input(
                    "Per-Team Budget ($) *", min_value=0.0, step=10.0, value=None,
                    placeholder="e.g. 500.00"
                )
            add_btn = st.form_submit_button("Add Project", use_container_width=True)

        if add_btn:
            if not new_name.strip():
                st.error("Project name is required.")
            elif new_budget is None or new_budget < 0:
                st.error("Please enter a valid budget amount.")
            else:
                add_course_project(new_name, float(new_budget))
                st.success(f"Project **{new_name}** added with budget ${new_budget:.2f}.")
                st.rerun()

    # ── Existing projects table + edit ────────────────────────────────────
    projects = get_course_projects()

    if projects.empty:
        st.info("No course projects yet. Add one above.")
        return

    st.subheader("Existing Projects")
    st.dataframe(
        projects.rename(columns={"id": "ID", "name": "Project Name", "budget": "Per-Team Budget ($)"}),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("Edit or Delete a Project")

    project_map = dict(zip(projects["name"], projects["id"]))
    selected_name = st.selectbox("Select project", list(project_map.keys()))
    selected_row = projects[projects["name"] == selected_name].iloc[0]

    edit_col1, edit_col2 = st.columns(2)
    with edit_col1:
        edit_name = st.text_input("New name", value=selected_row["name"], key="edit_name")
    with edit_col2:
        edit_budget = st.number_input(
            "New per-team budget ($)", min_value=0.0, step=10.0,
            value=float(selected_row["budget"]), key="edit_budget"
        )

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("Save Changes", type="primary", use_container_width=True):
            if not edit_name.strip():
                st.error("Project name cannot be empty.")
            else:
                update_course_project(int(selected_row["id"]), edit_name, edit_budget)
                st.success("Project updated.")
                st.rerun()
    with btn_col2:
        if st.button("Delete Project", type="secondary", use_container_width=True):
            delete_course_project(int(selected_row["id"]))
            st.warning(f"Project **{selected_name}** deleted.")
            st.rerun()


# Render the budget tracking page: per-team spending vs per-team budget, grouped by project
def page_budget_tracking() -> None:
    st.title("Budget Tracking")
    st.write(
        "Each course project has a **per-team budget**. "
        "This page tracks how much each team has spent within their project."
    )

    summary = get_budget_by_team()

    if summary.empty:
        st.info("No spending data yet. Budget rows will appear once students submit requests.")
        return

    # Colour-code the Remaining column
    def highlight_remaining(val: float) -> str:
        if val < 0:
            return "color: red; font-weight: bold"
        if val < 50:
            return "color: orange"
        return "color: green"

    styled = summary.style.format(
        {
            "Per-Team Budget ($)": "${:.2f}",
            "Spent ($)": "${:.2f}",
            "Remaining ($)": "${:.2f}",
        }
    ).applymap(highlight_remaining, subset=["Remaining ($)"])

    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.divider()
    t_col1, t_col2, t_col3 = st.columns(3)
    t_col1.metric("Total Allocated", f"${summary['Per-Team Budget ($)'].sum():.2f}")
    t_col2.metric("Total Spent", f"${summary['Spent ($)'].sum():.2f}")
    t_col3.metric("Total Remaining", f"${summary['Remaining ($)'].sum():.2f}")

    # Spending bar chart grouped by project+team label
    st.divider()
    st.subheader("Spending by Team")
    chart_df = summary.copy()
    chart_df["Label"] = chart_df["Project"] + " — Team " + chart_df["Team"].astype(str)
    chart_data = chart_df.set_index("Label")[["Per-Team Budget ($)", "Spent ($)"]]
    st.bar_chart(chart_data, color=["#4B2E83", "#F2A900"])


# Render the archive page showing all archived requests
def page_archive() -> None:
    st.title("Archived Requests")
    st.write("Historical view of all archived requests. No data is ever deleted.")

    df = get_archived_requests()

    if df.empty:
        st.info("No archived requests yet.")
        return

    team_options = ["All"] + sorted(df["team"].unique().tolist())
    selected_team = st.selectbox(
        "Filter by Team", team_options, key="archive_team_filter"
    )

    filtered = df.copy()
    if selected_team != "All":
        filtered = filtered[filtered["team"] == int(selected_team)]

    st.write(f"Showing **{len(filtered)}** archived record(s)")

    display_cols = [
        "id", "submitter_email", "team", "cfo_name", "course", "supplier",
        "item_name", "quantity", "unit_price", "total_price",
        "request_status", "created_at", "updated_at", "notes", "admin_notes",
    ]
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# App entry point
# ─────────────────────────────────────────────

# Bootstrap the database, enforce login, then route to the correct page by role
def main() -> None:
    st.set_page_config(
        page_title="Purchase Request Manager",
        page_icon="🛒",
        layout="wide",
    )

    # Inject custom CSS to keep sidebar text white on the UW purple background,
    # and highlight the selected nav item with GIX gold.
    st.markdown("""
<style>
/* ── 侧边栏 ─────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #4B2E83 !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] label[data-checked="true"] {
    background-color: #F2A900 !important;
    border-radius: 4px;
    color: #1A1A1A !important;
}
[data-testid="stSidebar"] button {
    background-color: #F2A900 !important;
    border-color: #F2A900 !important;
    color: #1A1A1A !important;
}

/* ── 全局 primary 按钮 ──────────────────────── */
button[kind="primary"],
[data-testid="stFormSubmitButton"] button,
button[data-testid="baseButton-primary"] {
    background-color: #F2A900 !important;
    border-color: #F2A900 !important;
    color: #1A1A1A !important;
}
button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover,
button[data-testid="baseButton-primary"]:hover {
    background-color: #d49200 !important;
    border-color: #d49200 !important;
}

/* ── 选中 / 活跃色 ──────────────────────────── */
[data-baseweb="radio"] [data-checked="true"] div,
[data-baseweb="checkbox"] [data-checked="true"] div {
    background-color: #F2A900 !important;
    border-color: #F2A900 !important;
}

/* ── 提示框（st.info / st.success）→ 浅紫 ──── */
[data-testid="stAlert"] {
    background-color: #EDE7F6 !important;
    border-color: #4B2E83 !important;
    color: #1A1A1A !important;
}
[data-testid="stAlert"] * {
    color: #1A1A1A !important;
}
/* st.warning → 浅金黄 */
[data-testid="stAlert"][data-baseweb="notification"][aria-label*="Warning"],
div:has(> [data-testid="stAlert"] svg[data-testid="stAlertDynamicIcon-warning"]) [data-testid="stAlert"],
[data-testid="stAlertContentWarning"] {
    background-color: #FFF8E1 !important;
    border-color: #F2A900 !important;
}

/* 通用 notification 容器（base-web）──────────── */
[data-baseweb="notification"] {
    background-color: #EDE7F6 !important;
    border-color: #4B2E83 !important;
}

/* ── Expander 背景 → 白色 ────────────────────── */
[data-testid="stExpander"] details {
    background-color: #FFFFFF !important;
    border-color: #c5b8e8 !important;
}
[data-testid="stExpander"] details > div {
    background-color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

    init_db()

    # ── Authentication gate ────────────────────────────────────────────────
    if "user" not in st.session_state:
        page_login()
        return

    user = st.session_state["user"]

    # ── Sidebar: user info + logout ────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"**{user['display_name'] or user['email']}**")
        st.caption(user["email"])
        role_badge = "🎓 Student" if user["role"] == "student" else "🔑 Admin"
        st.caption(role_badge)
        st.divider()

        # ── Navigation ─────────────────────────────────────────────────────
        if user["role"] == "student":
            page = st.radio(
                "Pages",
                ["Submit Request", "My Orders"],
            )
        else:
            page = st.radio(
                "Pages",
                [
                    "Dashboard",
                    "Course Project Setup",
                    "Budget Tracking",
                    "Archive",
                ],
            )

        st.divider()
        if st.button("Logout", use_container_width=True):
            del st.session_state["user"]
            st.rerun()

        st.caption("Purchase Request Manager v2.0")

    # ── Page routing ───────────────────────────────────────────────────────
    if user["role"] == "student":
        if page == "Submit Request":
            page_submission_form()
        elif page == "My Orders":
            page_my_orders()
    else:
        if page == "Dashboard":
            page_dashboard()
        elif page == "Course Project Setup":
            page_course_project_setup()
        elif page == "Budget Tracking":
            page_budget_tracking()
        elif page == "Archive":
            page_archive()


if __name__ == "__main__":
    main()
