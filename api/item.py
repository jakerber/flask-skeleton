"""Item API endpoints."""
from api import common
from db import database

def getItems():
    """Get items."""
    owner = common.parse('owner', int, optional=True)

    # fetch a single item by owner
    if owner:
        items = database.Item.query.filter_by(
            owner=owner).all()
        if not items:
            raise RuntimeError(f'no items found for {owner}')

    # fetch all items
    else:
        items = database.Item.query.all()

    return [item.dict() for item in items]

def createItem():
    """Create an item."""
    value = common.parse('value', str)
    owner = common.parse('owner', int)

    # create and insert an item
    newItem = database.Item(
        value=value,
        owner=owner).save()
    return newItem.dict()

def modifyItem():
    """Modify an item."""
    raise NotImplementedError

def deleteItem():
    """Delete an item."""
    id = common.parse('id', int)

    # fetch item
    item = database.Item.query.get(id)
    if not item:
        raise RuntimeError(f'item {id} not found')

    # delete item
    item.delete()
