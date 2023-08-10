#!/usr/bin/env python3
"""
Session Authentication
"""
import uuid
from .auth import Auth


class SessionAuth(Auth):
    """Session Authentication session"""
    user_id_by_session_id = {}

    def __init__(self):
        """Initialization"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Creates a session_id for a user_id"""
        if user_id is not None and isinstance(user_id, str):
            session_id = uuid.uuid4()
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a user ID based on a Session ID"""
        if session_id is not None or isinstance(session_id, str):
            user_id = SessionAuth.user_id_by_session_id.get(session_id)
            return user_id
        return None
