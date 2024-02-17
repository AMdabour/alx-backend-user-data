#!/usr/bin/env python3
"""session authentication with sessionAuth class"""
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session Authentication Class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session id for the given user"""
        if user_id is None or type(user_id) is not str:
            return None
        # Generate a unique session id
        session_id = str(uuid4())  # Create a random UUID
        self.user_id_by_session_id[session_id] = user_id
        return session_id
