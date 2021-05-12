"""User API endpoints."""
import database
from api import common

def getUsers():
    """Get users by phone number.

    :field phone [int]: user phone number
    :returns [dict|list]: user or list of users
    :raises RuntimeError: if no users exists with the phone number
    """
    phone = common.parse('phone', int, optional=True)
    if phone:
        user = database.User.query.get(phone)
        if not user:
            raise RuntimeError(f'user not found')
        return user.dict()
    return [user.dict() for user in database.User.query.all()]

def createUser():
    """Create a user.

    :field phone [int]: user phone number
    :field name [str]: user name
    :field password [str]: user password (will be encrypted)
    :returns [dict]: newly created user with auth token
    """
    phone = common.parse('phone', int)
    name = common.parse('name', str)
    password = common.parse('password', str)
    encryptedPassword = common.encrypt(password)
    newUser = database.User(phone=phone, name=name, password=encryptedPassword).save()
    newUserInfo = newUser.dict()
    newUserInfo['token'] = common.tokenize(newUser)
    return newUserInfo

def modifyUserName():
    """Modify a user's name.

    :field phone [int]: user phone number
    :field name: name to update
    :raises RuntimeError: if no user exists with the phone number
    :returns [dict]: updated user
    """
    phone = common.parse('phone', int)
    name = common.parse('name', str)
    user = database.User.query.get(phone)
    if not user:
        raise RuntimeError(f'user not found')
    user.name = name
    user.save()
    return user.dict()

def deleteUser():
    """Delete a user by phone number.

    :field phone [int]: user phone number
    :field password [str]: user password (will be encrypted)
    :raises RuntimeError: if no user exists with the phone number and password
    """
    phone = common.parse('phone', int)
    password = common.parse('password', str)
    user = database.User.query.get(phone)
    if not user:
        raise RuntimeError(f'user not found')
    if user.password != common.encrypt(password):
        raise RuntimeError(f'incorrect password')

    # TODO: delete user's items

    user.delete()
