"""Authentication API endpoints."""
import database
from api import common

def signIn():
    """Sign in a user.

    :field phone [int]: user's phone number
    :field password [str]: user's password (will be encrypted)
    :raises AuthenticationError: if no user exists with the phone number and password
    :returns [str]: authentication token
    """
    phone = common.parse('phone', int)
    password = common.parse('password', str)
    user = database.User.query.filter_by(phone=phone).first()
    if not user:
        raise common.AuthenticationError('user does not exist')
    if user.password != common.encrypt(password):
        raise common.AuthenticationError('incorrect password')
    return common.tokenize(user)

def signOut():
    """Sign out a user."""
    raise NotImplementedError  # TODO

def signUp():
    """Sign up a new user.

    :field phone [int]: user phone number
    :field name [str]: user name
    :field password [str]: user password (will be encrypted)
    :returns [dict]: newly created user's info with auth token
    """
    phone = common.parse('phone', int)
    name = common.parse('name', str)
    password = common.parse('password', str)
    encryptedPassword = common.encrypt(password)
    newUser = database.User(phone=phone, name=name, password=encryptedPassword).save()
    newUserInfo = newUser.dict()
    newUserInfo['auth_token'] = common.tokenize(newUser)  # attach auth token to response
    return newUserInfo
