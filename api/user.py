"""User API endpoints."""
import database
from api import common


def deleteUser():
    """Delete a user.

    :field password [str]: user password (will be encrypted)
    :raises RuntimeError: if password is incorrect
    """
    user = common.authenticate()
    password = common.parse('password', str)
    if user.password != common.encrypt(password):
        raise RuntimeError('incorrect password')

    # Delete all stuff owned by user
    for stuff in database.Stuff.query.filter_by(user_id=user.id).all():
        stuff.delete()

    user.delete()


def getAllUsers():
    """Get all existing users.

    Does not authenticate - not exposed in production.

    :returns [list]: user info as dicts
    """
    return [user.dict() for user in database.User.query.all()]


def getUser():
    """Get user.

    :returns [dict]: user info
    """
    user = common.authenticate()
    return user.dict()


def updateUser():
    """Update a user's information.

    :field name []: updated name (optional)
    :field phone [int]: updated phone number (optional)
    :returns [dict]: updated user info
    :raises ValueError: if no user info to update is provided
    """
    user = common.authenticate()
    name = common.parse('name', str, optional=True)
    phone = common.parse('phone', int, optional=True)
    if not name and not phone:
        raise ValueError('must provide name or phone to update')
    user.name = name or user.name
    user.phone = phone or user.phone
    user.save()
    return user.dict()
