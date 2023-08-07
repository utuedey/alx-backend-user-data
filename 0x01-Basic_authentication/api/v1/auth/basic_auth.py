#!/usr/bin/env python3
"""
basic_auth module
"""
from .auth import Auth
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
