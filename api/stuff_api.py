"""Stuff API endpoints."""
from db import models
from utils import auth_utils
import errors
from utils import request_utils


def createStuff():
    """Create stuff.

    :field description [str]: description of stuff
    :return [dict]: newly created stuff
    """
    user = auth_utils.authenticate()
    description = request_utils.parse('description', str)
    newStuff = models.Stuff(description=description, user_id=user.id).save()
    return newStuff.dict()


def deleteStuff():
    """Delete stuff by id.

    :field id [int]: stuff id
    :raises UnprocessableRequest: if owner is invalid or stuff does not exist
    """
    user = auth_utils.authenticate()
    id = request_utils.parse('id', int)
    stuff = models.Stuff.query.get(id)
    if not stuff:
        raise errors.UnprocessableRequest(f'no stuff found with id {id}')
    if stuff.user_id != user.id:
        raise errors.UnprocessableRequest('invalid owner')
    stuff.delete()


def getAllStuff():
    """Get all existing stuff.

    Does not authenticate - not exposed in production.

    :returns [list]: stuff as dicts
    """
    return [entry.dict() for entry in models.Stuff.query.all()]


def getStuff():
    """Get stuff by owner.

    :returns [list]: stuff as dicts
    """
    user = auth_utils.authenticate()
    stuff = models.Stuff.query.filter_by(user_id=user.id).all()
    return [entry.dict() for entry in stuff]


def updateStuff():
    """Update stuff.

    :field id [int]: stuff id
    :field description [str]: description to update
    :raises UnprocessableRequest: if owner is invalid or stuff does not exist
    :returns [dict]: updated stuff
    """
    user = auth_utils.authenticate()
    id = request_utils.parse('id', int)
    newDescription = request_utils.parse('description', str)
    stuff = models.Stuff.query.get(id)
    if not stuff:
        raise errors.UnprocessableRequest(f'no stuff found with id {id}')
    if stuff.user_id != user.id:
        raise errors.UnprocessableRequest('invalid owner')
    stuff.description = newDescription
    stuff.save()
    return stuff.dict()
