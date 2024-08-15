#!/usr/bin/env python3
"""
Main file
restart server before each test
"""
import requests


def register_user(email: str, password: str) -> None:
    """ test user registration
    """
    expected = {'email': email, 'message': 'user created'}
    form = {'email': email, 'password': password}
    r = requests.post('http://0.0.0.0:5000/users', data=form)
    assert r.status_code == 200
    assert r.json() == expected


def log_in_wrong_password(email: str, password: str) -> None:
    """ test wrong password login
    """
    form = {'email': email, 'password': password}
    r = requests.post('http://0.0.0.0:5000/sessions', data=form)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ test log_in
    """
    expected = {'email': email, 'message': 'logged in'}
    form = {'email': email, 'password': password}
    r = requests.post('http://0.0.0.0:5000/sessions', data=form)
    assert r.status_code == 200
    assert r.json() == expected
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """tesr profile_unlogged
    """
    r = requests.get('http://0.0.0.0:5000/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """ test profile_logged
    """
    expected = {'email': 'guillaume@holberton.io'}
    cookies = {'session_id': session_id}
    r = requests.get('http://0.0.0.0:5000/profile', cookies=cookies)
    assert r.status_code == 200
    assert r.json() == expected


def log_out(session_id: str) -> None:
    """ test logout
    """
    expected = {'message': 'Bienvenue'}
    cookies = {'session_id': session_id}
    r = requests.delete('http://0.0.0.0:5000/sessions', cookies=cookies)
    assert r.status_code == 200
    assert r.json() == expected


def reset_password_token(email: str) -> str:
    """ test reset password token
    """
    form = {'email': email}
    r = requests.post('http://0.0.0.0:5000/reset_password', data=form)
    assert r.status_code == 200
    return r.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test update password
    """
    expected = {'email': email, 'message': 'Password updated'}
    form = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put('http://0.0.0.0:5000/reset_password', data=form)
    assert r.json() == expected


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
