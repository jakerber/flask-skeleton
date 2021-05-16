"""User API endpoints."""
from db import models
from utils import auth_utils
import errors
from utils import request_utils


def deleteUser():
    """Delete an authenticated user.

    :field password [str]: user password (will be encrypted)
    :raises UnprocessableRequest: if password is incorrect
    """
    user = auth_utils.authenticate()
    password = request_utils.parse('password', str)
    if user.password != auth_utils.encrypt(password):
        raise errors.UnprocessableRequest('incorrect password')

    # Delete all stuff owned by user
    for stuff in models.Stuff.query.filter_by(user_id=user.id).all():
        stuff.delete()

    user.delete()


def getUser():
    """Get authenticated user.

    :returns [dict]: user info
    """
    user = auth_utils.authenticate()
    return user.dict()


def updateUser():
    """Update authenticated user info.

    :field name [str]: updated name (optional)
    :field phone [int]: updated phone number (optional)
    :returns [dict]: updated user info
    :raises MissingParameter: if no user info to update is provided
    """
    user = auth_utils.authenticate()
    name = request_utils.parse('name', str, optional=True)
    phone = request_utils.parse('phone', int, optional=True)
    if not name and not phone:
        raise errors.MissingParameter('must provide name or phone to update')
    user.name = name or user.name
    user.phone = phone or user.phone
    user.save()
    return user.dict()
