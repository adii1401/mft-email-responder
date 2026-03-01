import os
import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Follow-up Tracker", page_icon="📋", layout="wide")

DB_PATH = "./data/followups.db"

# ─── SLA deadlines by priority ───────────────────────────────────
SLA_HOURS = {
    "P1 - Production Down": 2,
    "P2 - Degraded Service": 4,
    "P3 - Non-critical": 24,
    "P4 - General Query": 48
}

# ─── DB Setup ────────────────────────────────────────────────────
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS followups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            sender TEXT,
            sent_at TEXT,
            reply_summary TEXT,
            priority TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'Pending',
            notes TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

def get_all_followups():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM followups ORDER BY deadline ASC", conn)
    conn.close()
    return df

def add_followup(subject, sender, reply_summary, priority):
    deadline = datetime.now() + timedelta(hours=SLA_HOURS[priority])
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO followups (subject, sender, sent_at, reply_summary, priority, deadline, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
    """, (
        subject,
        sender,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        reply_summary,
        priority,
        deadline.strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()

def update_status(followup_id, new_status, notes=""):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        UPDATE followups SET status = ?, notes = ? WHERE id = ?
    """, (new_status, notes, followup_id))
    conn.commit()
    conn.close()

def delete_followup(followup_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM followups WHERE id = ?", (followup_id,))
    conn.commit()
    conn.close()

def get_status_color(status, deadline_str):
    now = datetime.now()
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        overdue = now > deadline
    except:
        overdue = False

    if status == "Resolved":
        return "🟢"
    elif status == "Escalated":
        return "🔴"
    elif overdue:
        return "🔴"
    else:
        return "🟡"

# ─── Init DB ─────────────────────────────────────────────────────
init_db()

# ─── UI ──────────────────────────────────────────────────────────
st.title("📋 MFT Support — Follow-up Tracker")
st.markdown("Track pending replies, SLA deadlines, and resolution status.")

# ─── Summary metrics ─────────────────────────────────────────────
df = get_all_followups()

col1, col2, col3, col4 = st.columns(4)
total = len(df)
pending = len(df[df["status"] == "Pending"]) if total > 0 else 0
resolved = len(df[df["status"] == "Resolved"]) if total > 0 else 0
escalated = len(df[df["status"] == "Escalated"]) if total > 0 else 0

now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
overdue = len(df[(df["status"] == "Pending") & (df["deadline"] < now_str)]) if total > 0 else 0

col1.metric("Total", total)
col2.metric("Pending", pending)
col3.metric("Resolved", resolved)
col4.metric("🔴 Overdue", overdue)

st.divider()

# ─── Add manual follow-up ─────────────────────────────────────────
with st.expander("➕ Add Manual Follow-up"):
    with st.form("add_form"):
        m_subject = st.text_input("Email Subject")
        m_sender = st.text_input("Sender Email")
        m_summary = st.text_area("Reply Summary", height=80)
        m_priority = st.selectbox("Priority", list(SLA_HOURS.keys()))
        submitted = st.form_submit_button("Add Follow-up")
        if submitted and m_subject and m_sender:
            add_followup(m_subject, m_sender, m_summary, m_priority)
            st.success("✅ Follow-up added!")
            st.rerun()

st.divider()

# ─── Filter ──────────────────────────────────────────────────────
status_filter = st.selectbox("Filter by status", ["All", "Pending", "Resolved", "Escalated", "🔴 Overdue only"])

# ─── Follow-up list ──────────────────────────────────────────────
df = get_all_followups()

if df.empty:
    st.info("No follow-ups yet. They will appear here automatically when you send replies from the main app.")
else:
    # Apply filter
    if status_filter == "Pending":
        df = df[df["status"] == "Pending"]
    elif status_filter == "Resolved":
        df = df[df["status"] == "Resolved"]
    elif status_filter == "Escalated":
        df = df[df["status"] == "Escalated"]
    elif status_filter == "🔴 Overdue only":
        df = df[(df["status"] == "Pending") & (df["deadline"] < now_str)]

    st.markdown(f"**{len(df)} item(s) shown**")

    for _, row in df.iterrows():
        status_icon = get_status_color(row["status"], row["deadline"])
        is_overdue = row["status"] == "Pending" and row["deadline"] < now_str
        overdue_tag = " ⚠️ OVERDUE" if is_overdue else ""

        with st.expander(f"{status_icon} {row['subject']} — {row['sender']} ({row['sent_at']}){overdue_tag}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Priority:** {row['priority']}")
                st.markdown(f"**Deadline:** {row['deadline']}")
                st.markdown(f"**Status:** {row['status']}")
            with col_b:
                st.markdown(f"**Sent at:** {row['sent_at']}")
                st.markdown(f"**Sender:** {row['sender']}")

            st.markdown(f"**Reply Summary:** {row['reply_summary']}")

            if row["notes"]:
                st.markdown(f"**Notes:** {row['notes']}")

            st.divider()

            # ─── Status update ───────────────────────────────────
            if row["status"] != "Resolved":
                col1_btn, col2_btn, col3_btn = st.columns(3)
                with col1_btn:
                    if st.button("✅ Mark Resolved", key=f"resolve_{row['id']}"):
                        update_status(row["id"], "Resolved")
                        st.rerun()
                with col2_btn:
                    if st.button("🔺 Escalate", key=f"escalate_{row['id']}"):
                        update_status(row["id"], "Escalated")
                        st.rerun()
                with col3_btn:
                    if st.button("🗑️ Delete", key=f"delete_{row['id']}"):
                        delete_followup(row["id"])
                        st.rerun()

                notes_input = st.text_input("Add note:", key=f"notes_{row['id']}")
                if notes_input:
                    if st.button("💾 Save Note", key=f"save_note_{row['id']}"):
                        update_status(row["id"], row["status"], notes_input)
                        st.rerun()
            else:
                if st.button("🗑️ Delete", key=f"delete_resolved_{row['id']}"):
                    delete_followup(row["id"])
                    st.rerun()

st.divider()

# ─── SQL Console ─────────────────────────────────────────────────
st.subheader("🗄️ SQL Console")
st.markdown("Run raw SQL queries against the follow-ups database.")

default_query = "SELECT * FROM followups ORDER BY sent_at DESC"
sql_input = st.text_area("SQL Query:", value=default_query, height=80)

if st.button("▶️ Run Query"):
    try:
        conn = sqlite3.connect(DB_PATH)
        result_df = pd.read_sql_query(sql_input, conn)
        conn.close()
        st.success(f"{len(result_df)} row(s) returned")
        st.dataframe(result_df, use_container_width=True)
    except Exception as e:
        st.error(f"SQL Error: {e}")

with st.expander("💡 Example queries"):
    st.code("SELECT * FROM followups WHERE status = 'Pending'")
    st.code("SELECT * FROM followups WHERE deadline < datetime('now')")
    st.code("SELECT sender, COUNT(*) as total FROM followups GROUP BY sender")
    st.code("SELECT priority, COUNT(*) as total FROM followups GROUP BY priority")
    st.code("UPDATE followups SET status = 'Resolved' WHERE id = 1")