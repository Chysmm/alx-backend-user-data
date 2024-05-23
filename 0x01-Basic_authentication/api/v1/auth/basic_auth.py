#!/usr/bin/env python3
"""
Module for Basic API authentication
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class to manage the API authentication
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.

        Args:
            authorization_header (str): The authorization header string.

        Returns:
            str: The Base64 part of the authorization header or None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str):
            The Base64 authorization header string.

        Returns:
            str: The decoded value of the Base64 string or None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str):
            The Base64 decoded authorization header string.

        Returns:
            tuple: A tuple containing user email and password or (None, None).
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        usr_email, usr_pwd = decoded_base64_authorization_header.split(':', 1)
        return usr_email, usr_pwd

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance or None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request.

        Args:
            request: The Flask request object.

        Returns:
            User: The User instance or None.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None

        user_email, user_password = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_password is None:
            return None

        return self.user_object_from_credentials(user_email, user_password)
