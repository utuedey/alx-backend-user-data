#!/usr/bin/env python3
"""
encrypt_password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate hased password
    Args:
      hashed_password: bytes type
      password: string type
    Returns:
        bool
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
