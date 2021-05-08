"""Item API endpoints."""
import database
from api import common

def getItems():
    """Get items by owner.

    :field owner [int]: owner identifier (phone number)
    :returns [list]: items as dicts
    :raises RuntimeError: if no items exist with the owner
    """
    owner = common.parse('owner', int, optional=True)
    if owner:
        items = database.Item.query.filter_by(owner=owner).all()
    else:
        items = database.Item.query.all()
    return [item.dict() for item in items]

def createItem():
    """Create an item.

    :field value [str]: item value
    :field owner [int]: owner phone number (user primary key)
    :return [dict]: newly created item
    """
    value = common.parse('value', str)
    owner = common.parse('owner', int)
    newItem = database.Item(value=value, owner=owner).save()
    return newItem.dict()

def modifyItem():
    """Modify an item."""
    raise NotImplementedError

def deleteItem():
    """Delete an item by id.

    :field id [int]: item id
    :raises RuntimeError: if no item exists with the id
    """
    id = common.parse('id', int)
    item = database.Item.query.get(id)
    if not item:
        raise RuntimeError(f'item {id} not found')
    item.delete()
