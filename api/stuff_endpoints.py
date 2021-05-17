"""Stuff API endpoint functions."""
import errors
from db import models
from utils import authenticator
from utils import handler


def createStuff():
    """Create stuff.

    :field description [str]: description of stuff
    :return [dict]: newly created stuff
    """
    user = authenticator.authenticate()
    description = handler.parse('description', str)
    newStuff = models.Stuff(description=description, user_id=user.id).save()
    return newStuff.dict()


def deleteStuff():
    """Delete stuff by id.

    Administrators can execute.

    :field id [int]: stuff id
    :raises UnprocessableRequest: if owner is invalid or stuff does not exist
    """
    user = authenticator.authenticate()
    id = handler.parse('id', int)
    stuff = models.Stuff.query.get(id)
    if not stuff:
        raise errors.UnprocessableRequest(f'no stuff found with id {id}')
    if stuff.user_id != user.id and not user.is_admin:
        raise errors.UnprocessableRequest('invalid owner')
    stuff.delete()


def getStuff():
    """Get stuff by authenticated owner.

    :returns [list]: stuff as dicts
    """
    user = authenticator.authenticate()
    stuff = models.Stuff.query.filter_by(user_id=user.id).all()
    return [entry.dict() for entry in stuff]


def updateStuff():
    """Update stuff by id.

    Administrators can execute.

    :field id [int]: stuff id
    :field description [str]: description to update
    :raises UnprocessableRequest: if owner is invalid or stuff does not exist
    :returns [dict]: updated stuff
    """
    user = authenticator.authenticate()
    id = handler.parse('id', int)
    newDescription = handler.parse('description', str)
    stuff = models.Stuff.query.get(id)
    if not stuff:
        raise errors.UnprocessableRequest(f'no stuff found with id {id}')
    if stuff.user_id != user.id and not user.is_admin:
        raise errors.UnprocessableRequest('invalid owner')
    stuff.description = newDescription
    stuff.save()
    return stuff.dict()
