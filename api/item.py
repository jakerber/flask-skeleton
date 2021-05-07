"""Item API endpoints."""
from api import common
from db import database

def getItems():
    """Get items."""
    try:
        owner = common.parse('owner', int, optional=True)
    except ValueError as error:
        return common.failure(str(error))

    # fetch a single item by owner
    if owner:
        try:
            items = database.Item.query.filter_by(
                owner=owner).all()
        except Exception as error:
            return common.failure(repr(error))
        if not items:
            return common.failure(f'no items found for {owner}')

    # fetch all items
    else:
        try:
            items = database.Item.query.all()
        except Exception as error:
            return common.failure(repr(error))

    return common.success([item.dict() for item in items])

def createItem():
    """Create an item."""
    try:
        value = common.parse('value', str)
        owner = common.parse('owner', int)
    except ValueError as error:
        return common.failure(str(error))

    # create and insert an item
    try:
        newItem = database.Item(
            value=value,
            owner=owner).save()
    except Exception as error:
        return common.failure(repr(error))
    return common.success(newItem.dict())

def modifyItem():
    """Modify an item."""
    raise NotImplementedError  # TODO

def deleteItem():
    """Delete an item."""
    try:
        id = common.parse('id', int)
    except ValueError as error:
        return common.failure(str(error))

    # fetch item
    try:
        item = database.Item.query.get(id)
    except Exception as error:
        return common.failure(repr(error))
    if not item:
        return common.failure('item not found')

    # delete item
    try:
        item.delete()
    except Exception as error:
        return common.failure(repr(error))
    return common.success()
