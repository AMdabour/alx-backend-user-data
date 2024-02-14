#!/usr/bin/env python3
"""BasicAuth class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
        """extract base64 authorization header"""
        if authorization_header is None or \
                type(authorization_header) is not str or \
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(" ")[1]
