import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

STUDENT_FILE = "students.json"
LEAVE_FILE = "leave_data.json"
AUDIT_FILE = "audit_log.json"

# -----------------------------
# Load & Save JSON
# -----------------------------
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

students = load_json(STUDENT_FILE)
leave_data = load_json(LEAVE_FILE)
audit_data = load_json(AUDIT_FILE)

# -----------------------------
# Login
# -----------------------------
st.sidebar.title("Login")
role = st.sidebar.selectbox("Select Role", ["Admin", "Counsellor", "Professor", "HOD"])

if role != "Admin":
    st.error("Admin Access Only (Prototype Mode)")
    st.stop()

# -----------------------------
# Title
# -----------------------------
st.title("🚀 Leave Management Admin Dashboard")

# -----------------------------
# Metrics
# -----------------------------
total = len(leave_data)
approved = len([x for x in leave_data if x["status"] == "Approved"])
rejected = len([x for x in leave_data if x["status"] == "Rejected"])
pending = len([x for x in leave_data if x["status"] == "Pending"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Requests", total)
col2.metric("Approved", approved)
col3.metric("Rejected", rejected)
col4.metric("Pending", pending)

st.divider()

# -----------------------------
# Student Database
# -----------------------------
st.subheader("🎓 Student Database")

student_df = pd.DataFrame(students)
search_student = st.text_input("Search Student Name")

if search_student:
    student_df = student_df[student_df["name"].str.contains(search_student, case=False)]

st.dataframe(student_df)

# Low Leave Warning
for student in students:
    if student["leave_balance"] < 3:
        st.warning(f"{student['name']} has low leave balance!")

st.divider()

# -----------------------------
# Leave Requests
# -----------------------------
st.subheader("📄 Leave Requests")

if leave_data:
    df = pd.DataFrame(leave_data)

    # Add Stage & AI confidence if missing
    if "current_stage" not in df.columns:
        df["current_stage"] = "Counsellor"

    if "ai_confidence" not in df.columns:
        df["ai_confidence"] = 0.90

    # Filters
    search = st.text_input("Search Leave by Student Name")
    if search:
        df = df[df["student_name"].str.contains(search, case=False)]

    st.dataframe(df)

    # Pie Chart
    st.subheader("📊 Leave Status Distribution")
    status_counts = df["status"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%")
    st.pyplot(fig)

    # CSV Export
    if st.button("Download Report CSV"):
        df.to_csv("leave_report.csv", index=False)
        st.success("Report Saved as leave_report.csv")

    st.divider()

    # -----------------------------
    # Override Section
    # -----------------------------
    st.subheader("✏ Override Leave")

    selected_index = st.selectbox(
        "Select Leave",
        range(len(leave_data)),
        format_func=lambda x: f"{leave_data[x]['student_name']} - {leave_data[x]['status']}"
    )

    new_status = st.selectbox("New Status", ["Approved", "Rejected"])
    reason = st.text_input("Override Reason")

    if st.button("Apply Override"):
        leave_data[selected_index]["status"] = new_status

        # Calculate leave days properly
        from_date = datetime.strptime(
            leave_data[selected_index]["from_date"], "%Y-%m-%d"
        )
        to_date = datetime.strptime(
            leave_data[selected_index]["to_date"], "%Y-%m-%d"
        )

        days = (to_date - from_date).days + 1

        # Deduct balance if approved
        if new_status == "Approved":
            student_id = leave_data[selected_index]["student_id"]
            for student in students:
                if student["student_id"] == student_id:
                    student["leave_balance"] -= days

        save_json(STUDENT_FILE, students)
        save_json(LEAVE_FILE, leave_data)

        # Audit Log
        audit_entry = {
            "student_id": leave_data[selected_index]["student_id"],
            "action": "Override",
            "new_status": new_status,
            "reason": reason,
            "role_used": role,
            "timestamp": str(datetime.now())
        }

        audit_data.append(audit_entry)
        save_json(AUDIT_FILE, audit_data)

        st.success("Leave Updated Successfully")
        st.rerun()

else:
    st.info("No Leave Requests Found")

st.divider()

# -----------------------------
# Audit Logs
# -----------------------------
st.subheader("📝 Audit Logs")

if audit_data:
    st.dataframe(pd.DataFrame(audit_data))
else:
    st.info("No Audit Logs Found")