import bcrypt

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

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))