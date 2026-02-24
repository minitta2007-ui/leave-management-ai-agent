import sqlite3
from datetime import datetime


# ---------------- DATABASE UPDATE ---------------- #

def update_database(state, role=None, decision=None):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO leave_requests
        (id, student_id, days, current_stage, final_status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        state["leave_id"],
        state["student_id"],
        state["days"],
        state["current_stage"],
        state["final_status"]
    ))

    if role and decision:
        cursor.execute("""
            INSERT INTO approval_logs
            (leave_id, role, decision, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            state["leave_id"],
            role,
            decision,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()


# ---------------- STAGE VALIDATION ---------------- #

def check_db_stage(leave_id, expected_stage):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT current_stage FROM leave_requests WHERE id = ?",
        (leave_id,)
    )

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False

    return result[0] == expected_stage


# ---------------- STATE CREATION ---------------- #

def create_state(data):
    return {
        "leave_id": data["leave_id"],
        "student_id": data["student_id"],
        "days": data["days"],
        "confidence": data["confidence"],
        "policy_allowed": data["policy_allowed"],
        "current_stage": "validate",
        "final_status": None
    }


# ---------------- AUTO RULE CHECK ---------------- #

def rule_check(state):
    if (
        state["days"] <= 3 and
        state["confidence"] > 0.85 and
        state["policy_allowed"]
    ):
        state["final_status"] = "Approved"
        state["current_stage"] = "Completed"
    else:
        state["current_stage"] = "counsellor"

    update_database(state)
    return state


# ---------------- PROCESS ENTRY ---------------- #

def process_leave(data):
    state = create_state(data)
    state = rule_check(state)
    return state


# ---------------- COUNSELLOR ---------------- #

def counsellor_action(state, decision):
    if not check_db_stage(state["leave_id"], "counsellor"):
        return {"error": "Stage Skipping Attempt"}

    if decision == "Approved":
        state["current_stage"] = "professor"
    else:
        state["final_status"] = "Rejected"
        state["current_stage"] = "Completed"

    update_database(state, "Counsellor", decision)
    return state


# ---------------- PROFESSOR ---------------- #

def professor_action(state, decision):
    if not check_db_stage(state["leave_id"], "professor"):
        return {"error": "Stage Skipping Attempt"}

    if decision == "Approved":
        state["current_stage"] = "hod"
    else:
        state["final_status"] = "Rejected"
        state["current_stage"] = "Completed"

    update_database(state, "Professor", decision)
    return state


# ---------------- HOD ---------------- #

def hod_action(state, decision):
    if not check_db_stage(state["leave_id"], "hod"):
        return {"error": "Stage Skipping Attempt"}

    if decision == "Approved":
        state["final_status"] = "Approved"
    else:
        state["final_status"] = "Rejected"

    state["current_stage"] = "Completed"

    update_database(state, "HOD", decision)
    return state