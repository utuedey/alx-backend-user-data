#!/usr/bin/env python3
"""
Handles all routes for session Authentication
"""
import os
from flask import Flask, request
from typing import Tuple

from models.user import User
from api.v1.views import app_views


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /auth_session/login
    Return:
      - json rep of a User instance
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if users[0].is_valid_password(password):
        from ap.vi.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return res
    return jsonify({"error": "wrong password"}), 401
