#!/usr/bin/env python3
"""Auth class for handling authentication with the API."""
from flask import request
from typing import List, TypeVar
# from models.user import User


class Auth:
    """Auth class"""
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """authenticate"""
        return False

    def authorization_header(self, request=None) -> str:
        """auth header"""
        return None

    User = TypeVar('User')

    def current_user(self, request=None) -> User:
        """current user"""
        return None
