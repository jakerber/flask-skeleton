"""Stuff API endpoints."""
import database
from api import common

def createStuff():
    """Create stuff.

    :field description [str]: description of stuff
    :return [dict]: newly created stuff
    """
    user = common.authenticate()
    description = common.parse('description', str)
    newStuff = database.Stuff(description=description, user_id=user.id).save()
    return newStuff.dict()

def deleteStuff(auth):
    """Delete stuff by id.

    :field id [int]: stuff id
    :raises ValueError: if stuff has incorrect owner
    """
    user = common.authenticate()
    id = common.parse('id', int)
    stuff = database.Stuff.query.get(id)
    if stuff.user_id != user.id:
        raise ValueError('incorrect owner')
    stuff.delete()

def getAllStuff():
    """Get all existing stuff.

    Does not authenticate - not exposed in production.

    :returns [list]: stuff as dicts
    """
    return [item.dict() for item in database.Stuff.query.all()]

def getStuff():
    """Get stuff by owner.

    :returns [list]: stuff as dicts
    """
    user = common.authenticate()
    stuff = database.Stuff.query.filter_by(user_id=user.id).all()
    return [item.dict() for item in stuff]

def updateStuff():
    """Update stuff.

    :field id [int]: stuff id
    :field description [str]: description to update
    :raises ValueError: if stuff has incorrect owner
    :returns [dict]: updated stuff
    """
    user = common.authenticate()
    id = common.parse('id', int)
    newDescription = common.parse('description', str)
    stuff = database.Stuff.query.get(id)
    if stuff.user_id != user.id:
        raise ValueError('incorrect owner')
    stuff.description = newDescription
    stuff.save()
    return stuff.dict()
