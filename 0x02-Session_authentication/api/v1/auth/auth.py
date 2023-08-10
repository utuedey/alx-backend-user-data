#!/usr/bin/env python3
"""
auth module
A class that manages API authenticaton
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Class that manages API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if path requires authentication"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path += "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """validates all requests"""
        if request is not None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Gets the current user from request"""
        return None

    def session_cookie(self, request=None) -> str:
        """Retrieves a cookie value from a request"""
        if request is not None:
            cookie_name = os.getenv("SESSION_NAME")
            return request.cookies.get(cookie_name)
        return None
