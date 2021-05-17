"""Authentication API endpoint functions."""
import errors
import flask
from db import models
from utils import authenticator
from utils import handler


def signIn():
    """Sign in a user.

    :field phone [int]: user's phone number
    :field password [str]: user's password (will be encrypted)
    :raises AuthenticationError: if no user exists with the phone and password
    :returns [str]: authentication token
    """
    phone = handler.parse('phone', int)
    password = handler.parse('password', str)
    user = models.User.query.filter_by(phone=phone).first()
    if not user:
        raise errors.AuthenticationError(f'no user found with phone {phone}')
    if user.password != authenticator.encrypt(password):
        raise errors.AuthenticationError('incorrect password')
    return authenticator.tokenize(user)


def signOut():
    """Sign out an authenticated user.

    Blacklists user's current auth token.
    """
    authenticator.authenticate()
    token = flask.request.headers.get('auth_token')
    models.AuthTokenBlacklist(token=token).save()


def signUp():
    """Sign up a new user.

    :field phone [int]: user phone number
    :field name [str]: user name
    :field password [str]: user password (will be encrypted)
    :returns [dict]: newly created user's info with auth token
    """
    phone = handler.parse('phone', int)
    name = handler.parse('name', str)
    password = handler.parse('password', str)
    encryptedPassword = authenticator.encrypt(password)
    newUser = models.User(phone=phone,
                          name=name,
                          password=encryptedPassword).save()
    newUserInfo = newUser.dict()
    newUserInfo['auth_token'] = authenticator.tokenize(newUser)  # attach auth token
    return newUserInfo
