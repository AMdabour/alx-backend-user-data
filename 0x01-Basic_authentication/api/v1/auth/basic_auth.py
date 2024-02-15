#!/usr/bin/env python3
"""BasicAuth class"""
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import Tuple, TypeVar
from models import user
User = TypeVar('User')


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """decode a base64 string"""
        if base64_authorization_header is None or \
                type(base64_authorization_header) is not str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode()
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """Extract username and password from the user credentials"""
        decoded = decoded_base64_authorization_header
        if decoded is None or type(decoded) is not str \
                or ':' not in decoded:
            return (None, None)
        return tuple(decoded.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd:
                                     str) -> user:
        """returns user object for credentials if present"""
        if user_email is None or type(user_email) is not str or \
                user_pwd is None or type(user_pwd) is not str:
            return None
        # check if user exists
        result = user.User.search({'email': user_email})
        if result:
            for u in result:
                if u.is_valid_password(user_pwd):
                    return u
        return None
