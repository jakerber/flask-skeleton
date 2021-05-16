"""Authentication API endpoints."""
import flask
from utils import auth_utils
from utils import request_utils
import errors
from db import models


def signIn():
    """Sign in a user.

    :field phone [int]: user's phone number
    :field password [str]: user's password (will be encrypted)
    :raises AuthenticationError: if no user exists with the phone and password
    :returns [str]: authentication token
    """
    phone = request_utils.parse('phone', int)
    password = request_utils.parse('password', str)
    user = models.User.query.filter_by(phone=phone).first()
    if not user:
        raise errors.AuthenticationError(f'no user found with phone {phone}')
    if user.password != auth_utils.encrypt(password):
        raise errors.AuthenticationError('incorrect password')
    return auth_utils.tokenize(user)


def signOut():
    """Sign out a user.

    Blacklist's user's current auth token.
    """
    auth_utils.authenticate()
    token = flask.request.headers.get('auth_token')
    models.AuthTokenBlacklist(token=token).save()


def signUp():
    """Sign up a new user.

    :field phone [int]: user phone number
    :field name [str]: user name
    :field password [str]: user password (will be encrypted)
    :returns [dict]: newly created user's info with auth token
    """
    phone = request_utils.parse('phone', int)
    name = request_utils.parse('name', str)
    password = request_utils.parse('password', str)
    encryptedPassword = auth_utils.encrypt(password)
    newUser = models.User(phone=phone,
                            name=name,
                            password=encryptedPassword).save()
    newUserInfo = newUser.dict()
    newUserInfo['auth_token'] = auth_utils.tokenize(newUser)  # attach auth token
    return newUserInfo
