"""User API endpoint functions."""
import errors
from db import models
from utils import authenticator
from utils import handler


def deleteUser():
    """Delete an authenticated user.

    :field password [str]: user password (will be encrypted)
    :raises AuthenticationError: if password is incorrect
    """
    user = authenticator.authenticate()
    password = handler.parse('password', str)
    if user.password != authenticator.encrypt(password):
        raise errors.AuthenticationError('incorrect password')

    # Delete all stuff owned by user
    for stuff in models.Stuff.query.filter_by(user_id=user.id).all():
        stuff.delete()

    user.delete()


def getUser():
    """Get authenticated user.

    :returns [dict]: user info
    """
    user = authenticator.authenticate()
    return user.dict()


def updateUser():
    """Update authenticated user info.

    :field name [str]: updated name (optional)
    :field phone [int]: updated phone number (optional)
    :field password [str]: updated password (optional - will be encrypted)
    :returns [dict]: updated user info
    :raises MissingParameter: if no user info to update is provided
    """
    user = authenticator.authenticate()
    name = handler.parse('name', str, optional=True)
    phone = handler.parse('phone', int, optional=True)
    password = handler.parse('password', str, optional=True)
    if not name and not phone and not password:
        raise errors.MissingParameter('name|phone|password')
    user.name = name or user.name
    user.phone = phone or user.phone
    user.password = authenticator.encrypt(password) if password else user.password
    user.save()
    return user.dict()
