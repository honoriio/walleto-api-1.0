import uuid

SESSIONS = {}

def create_session(user_id: int):
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = user_id
    return session_id

