#!/usr/bin/env python3
"""
Hash a password using bcrypt
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """encrypt a password"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password
