"""Authentication API endpoints."""
import database
from api import common

def signIn():
    """Sign in a user.

    :field phone [int]: user's phone number
    :field password [str]: user's password (will be encrypted)
    :raises AuthenticationError: if no user exists with the phone number and password
    :returns [dict]: authentication token in format {'auth_token': <auth_token>}
    """
    phone = common.parse('phone', int)
    password = common.parse('password', str)
    user = database.User.query.filter_by(phone=phone).first()
    if not user:
        raise common.AuthenticationError('invalid phone number')
    if user.password != common.encrypt(password):
        raise common.AuthenticationError('incorrect password')
    return {'auth_token': common.tokenize(user)}

def signOut():
    """Sign out a user."""
    raise NotImplementedError  # TODO
