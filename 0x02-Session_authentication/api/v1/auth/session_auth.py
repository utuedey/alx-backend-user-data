#!/usr/bin/env python3
"""
Session Authentication
"""
import uuid
from .auth import Auth
from models.user import User
from flask import request


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

    def current_user(self, request=None) -> User:
        """Retrieves a user using a cookie value"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroy an authenticated session"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
