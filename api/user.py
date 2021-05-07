"""User API endpoints."""
from api import common
from db import database

def getUsers():
    """Get users."""
    try:
        phone = common.parse('phone', int, optional=True)
    except ValueError as error:
        return common.failure(str(error))

    # fetch a single user
    if phone:
        try:
            user = database.User.query.get(phone)
        except Exception as error:
            return common.failure(repr(error))
        if not user:
            return common.failure('user does not exist')
        return common.success(user.dict())

    # fetch all users
    try:
        users = database.User.query.all()
    except Exception as error:
        return common.failure(repr(error))
    return common.success([user.dict() for user in users])

def createUser():
    """Create a user."""
    try:
        phone = common.parse('phone', int)
        name = common.parse('name', str)
        password = common.parse('password', str)
    except ValueError as error:
        return common.failure(str(error))

    # create and insert a user
    try:
        newUser = database.User(
            phone=phone,
            name=name,
            password=common.encrypt(password)).save()
    except Exception as error:
        return common.failure(repr(error))
    return common.success(newUser.dict())

def modifyUser():
    """Modify a user."""
    raise NotImplementedError  # TODO

def deleteUser():
    """Delete a user."""
    try:
        phone = common.parse('phone', int)
    except ValueError as error:
        return common.failure(str(error))

    # fetch user
    try:
        user = database.User.query.filter_by(
            phone=phone).first()
    except Exception as error:
        return common.failure(repr(error))
    if not user:
        return common.failure('user does not exist')

    # delete user
    try:
        user.delete()
    except Exception as err:
        return common.failure(repr(err))
    return common.success()
