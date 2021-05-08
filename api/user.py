"""User API endpoints."""
from api import common
from db import database

def getUsers():
    """Get users."""
    phone = common.parse('phone', int, optional=True)

    # fetch a single user
    if phone:
        user = database.User.query.get(phone)
        if not user:
            raise RuntimeError(f'user {phone} does not exist')
        return user.dict()

    # fetch all users
    users = database.User.query.all()
    return [user.dict() for user in users]

def createUser():
    """Create a user."""
    phone = common.parse('phone', int)
    name = common.parse('name', str)
    password = common.parse('password', str)

    # create and insert a user
    newUser = database.User(
        phone=phone,
        name=name,
        password=common.encrypt(password)).save()
    return newUser.dict()

def modifyUser():
    """Modify a user."""
    raise NotImplementedError  # TODO

def deleteUser():
    """Delete a user."""
    phone = common.parse('phone', int)

    # fetch user
    user = database.User.query.filter_by(
        phone=phone).first()
    if not user:
        raise RuntimeError('user {phone} does not exist')

    # delete user
    user.delete()
