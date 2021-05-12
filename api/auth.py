"""Authentication API endpoints."""
import database
from api import common

def signIn():
    """Sign in a user.

    :field phone [int]: user phone number
    :field password [str]: user password (encrypted)
    :raises RuntimeError: if no user exists with the phone number and password
    :returns [str]: authentication key
    """
    phone = common.parse('phone', int)
    password = common.parse('password', str)
    user = database.User.query.get(phone)
    if not user:
        raise RuntimeError(f'user not found')
    if user.password != common.encrypt(password):
        raise RuntimeError(f'incorrect password')
    return {'token': common.tokenize(user)}

def signOut():
    """Sign out a user."""
    raise NotImplementedError  # TODO
