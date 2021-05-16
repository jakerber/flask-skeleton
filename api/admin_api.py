"""Admin API endpoints.

All endpoints require administrative privileges in production.
"""
import config
from db import models
from utils import auth_utils


def getAllStuff():
    """Get all existing stuff.

    :returns [list]: stuff as dicts
    """
    if config.FLASK_ENV == 'production':
        auth_utils.authenticate(admin=True)
    return [entry.dict() for entry in models.Stuff.query.all()]


def getBlacklistedTokens():
    """Get all blacklisted auth tokens.

    :returns [list]: blacklisted tokens
    """
    if config.FLASK_ENV == 'production':
        auth_utils.authenticate(admin=True)
    return [token.dict().get('token')
            for token in models.AuthTokenBlacklist.query.all()]


def getAllUsers():
    """Get all existing users.

    :returns [list]: user info as dicts
    """
    if config.FLASK_ENV == 'production':
        auth_utils.authenticate(admin=True)
    return [user.dict() for user in models.User.query.all()]
