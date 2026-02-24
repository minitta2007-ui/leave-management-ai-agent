from workflow_module.workflow_engine import (
    process_leave,
    counsellor_action,
    professor_action,
    hod_action
)

data = {
    "leave_id": 2,
    "student_id": "111",
    "days": 5,
    "confidence": 0.9,
    "policy_allowed": True
}

state = process_leave(data)
print("After Rule Check:", state)

# Counsellor rejects
state = counsellor_action(state, "Approved")
print("After Counsellor:", state)

# Only continue if not completed
if state.get("current_stage") == "professor":
    state = professor_action(state, "Approved")
    print("After Professor:", state)

if state.get("current_stage") == "hod":
    state = hod_action(state, "Approved")
    print("Final Result:", state)