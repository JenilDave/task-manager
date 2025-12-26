
def is_new_status_valid(current_status: str, new_status: str) -> bool:
    valid_transitions = {
        "pending": ["in_progress", "completed", "failed"],
        "in_progress": ["completed", "failed"],
        "completed": [],
        "failed": []
    }

    allowed_transitions = valid_transitions.get(current_status, [])
    return new_status in allowed_transitions