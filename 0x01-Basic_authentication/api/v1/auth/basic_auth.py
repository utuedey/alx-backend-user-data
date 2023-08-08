#!/usr/bin/env python3
"""
basic_auth module
"""
from .auth import Auth
from models.user import User
from typing import TypeVar
import base64
import binascii


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(
                                           self,
                                           authorization_header: str) -> str:
        """Return the encoded part of the authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
                                     self,
                                     base64_authorization_header: str) -> str:
        """Decodes the base64-encoded authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            res = base64.b64decode(base64_authorization_header, validate=True)
            return res.decode("utf-8")
        except binascii.Error:
            return None

    def extract_user_credentials(
                  self,
                  decoded_base64_authorization_header: str) -> (str, str):
        """Return user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header
        if ":" in decoded_base64_authorization_header:
            index = credentials.index(":")
            username = credentials[:index]
            password = credentials[index+1:]

            return username, password

    def user_object_from_credentials(
                            self,
                            user_email: str, user_pwd: str) -> TypeVar('User'):
        """Get a user using credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if len(users) <= 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Get user from request"""
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        user = self.user_object_from_credentials(email, password)

        return user
