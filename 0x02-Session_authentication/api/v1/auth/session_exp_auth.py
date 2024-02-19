#!/usr/bin/env python3
"""set expiration date to the session id"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """expiration"""
    def __init__(self) -> None:
        try:
            value = getenv('SESSION_DURATION')
            if value:
                self.session_duration = int(value)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overloads the create_session of sessionAUth"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        super().user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """search for user_id by session_id"""
        if session_id and super().user_id_by_session_id[session_id]:
            if self.session_duration <= 0:
                return super().user_id_by_session_id[session_id]['user_id']
            date = super().user_id_by_session_id[session_id]['created_at']
            duration = timedelta(seconds=self.session_duration)
            if date:
                if date + duration >= datetime.now():
                    return super().user_id_by_session_id[session_id]['user_id']
                return None
            return None
        return None
