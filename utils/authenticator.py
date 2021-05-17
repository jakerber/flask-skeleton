"""API authentication utility functions."""
import config
import datetime
import errors
import flask
import hashlib
import jwt
from db import models


def authenticate(admin=False):
    """Validate authentication token.

    :param admin [bool]: authenticate with admin privileges
    :header auth_token [str]: authentication token
    :returns user [User]: authenticated user's database object
    :raises MissingParameter: if auth token is missing from request header
    :raises AuthenticationError: if authentication fails
    """
    token = flask.request.headers.get('auth_token')
    if not token:
        raise errors.MissingParameter('auth_token')

    # Decode and verify token
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise errors.AuthenticationError('session expired')
    except jwt.DecodeError:
        raise errors.AuthenticationError('invalid token format')
    ipAddress = payload.get('ipa')
    if ipAddress != flask.request.remote_addr:
        raise errors.AuthenticationError(
            'mismatched ip address: tokenized address '
            '{ipAddress} != current address {flask.request.remote_addr}')

    # Ensure user is not signed out
    if models.AuthTokenBlacklist.query.get(token):
        raise errors.AuthenticationError('session ended')

    # Fetch user from token subject
    userId = payload.get('sub')
    user = models.User.query.get(userId)
    if not user:
        raise errors.AuthenticationError('user does not exist')

    # Verify user is an admin
    if models.Admin.query.filter_by(user_id=userId).first():
        user.is_admin = True
    elif admin:
        raise errors.AuthenticationError('user is not an admin')

    return user


def encrypt(password):
    """Encrypt a plain text password.

    :param password [str]: plain text password
    :returns [str]: SHA256-encrypted password
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def tokenize(user):
    """
    Generate an authentication token.

    https://realpython.com/token-based-authentication-with-flask/

    :param user [User]: user database model to authenticate
    :returns [str]: auth token
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            seconds=config.AUTH_TOKEN_LIFESPAN_SEC),  # expiration date
        'iat': datetime.datetime.utcnow(),  # time created
        'sub': user.id,  # subject
        'ipa': flask.request.remote_addr  # ip address
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
