#!/usr/bin/env python3
"""
Module for API authentication
"""
from flask import request
from typing import List, TypeVar
import fnmatch
import os


class Auth:
    """
    Auth class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Public method to check if a path requires authentication
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path has a trailing slash for comparison
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Handle wildcard in excluded paths
            if fnmatch.fnmatch(path, excluded_path):
                return False
            if excluded_path.endswith('*'):
                if fnmatch.fnmatch(path, excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Public method to get the authorization header from the request
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Public method to get the current user from the request
        """
        return None

    def session_cookie(self, request=None):
        """
        Return a cookie value from a request.

        Args:
            request: The Flask request object.

        Returns:
            The value of the cookie named by the SESSION_NAME
            environment variable from the request.
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        if session_name is None:
            return None
        return request.cookies.get(session_name)
