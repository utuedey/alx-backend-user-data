#!/usr/bin/env python3
"""
auth module
A class that manages API authenticaton
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class that manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Return bool"""
        return False

    def authorization_header(self, request=None) -> str:
        """Return None"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Return None"""
        return None
