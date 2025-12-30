def is_new_status_valid(current_status: str, new_status: str) -> bool:
    valid_transitions = {
        "CREATED": "IN_PROGRESS",
        "IN_PROGRESS": "BLOCKED",
        "BLOCKED": "IN_PROGRESS",
        "IN_PROGRESS": "COMPLETED",
    }

    allowed_transitions = valid_transitions.get(current_status, [])
    return new_status in allowed_transitions

def is_final_status(status: str) -> bool:
    return status == "COMPLETED"