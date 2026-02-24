from workflow_module.workflow_engine import (
    process_leave,
    counsellor_action,
    professor_action,
    hod_action
)

data = {
    "leave_id": 200,
    "student_id": "111",
    "days": 5,
    "confidence": 0.92,
    "policy_allowed": True
}

# Initial routing
state = process_leave(data)
print("After Rule Check:", state)

# Counsellor approves
state = counsellor_action(state, "Approved")
print("After Counsellor:", state)

# Professor approves
state = professor_action(state, "Approved")
print("After Professor:", state)

# HOD approves
state = hod_action(state, "Approved")
print("Final Result:", state)