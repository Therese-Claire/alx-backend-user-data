#!/usr/bin/env python3
""" auth module
"""
import uuid
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashes a user password

    Args:
        password (str): user's password
    Returns:
        bytes: bcrypt hashed string
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ generates a uuid and returns it
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initializes an Auth object
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user and save to the database

        Args:
            email (str): user's email
            password (str): user's password
        Returns:
            User: the newly created User object
        """
        try:
            self._db.find_user_by(**{'email': email})
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ validates if a user's login credentials

        Args:
            email (str): user's email
            password (str): user's password
        Returns:
            bool: True if user exist and password match.. otherwise False
        """
        try:
            user = self._db.find_user_by(**{'email': email})
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ creates and saves a user's session_id

        Args:
            email (str): user's email
        Returns:
            str: user's session_id
        """
        try:
            user = self._db.find_user_by(**{'email': email})
            self._db.update_user(user.id, session_id=_generate_uuid())
            return user.session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """ retrieves a user based on their session id

        Args:
            session_id (str): user's session_id
        Returns:
            User: the User object
        """
        try:
            return self._db.find_user_by(**{'session_id': session_id})
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """updates user session_id to None

        Args:
            user_id (int): user's id
        """
        self._db.update_user(user_id, **{'session_id': None})

    def get_reset_password_token(self, email: str) -> str:
        """ gets user's reset password token

        Args:
            email (str): user's email
        Returns:
            str: user's reset_token
        """
        try:
            user = self._db.find_user_by(**{'email': email})
            self._db.update_user(user.id, **{'reset_token': _generate_uuid()})
            return user.reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ resets a user's password

        Args:
            reset_token (str): user's password reset token
            password (str): user's password
        """
        try:
            user = self._db.find_user_by(**{'reset_token': reset_token})
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 **{'hashed_password': hashed_password,
                                    'reset_token': None})
        except Exception:
            raise ValueError
