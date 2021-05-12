"""Common API module."""
import constants
import database
import datetime
import hashlib
import flask
import jwt

# Exception type -> HTTP status code to respond with
# https://developer.mozilla.org/docs/Web/HTTP/Status
_EXCEPTION_TO_HTTP_STATUS_CODE = {
    'ValueError': 400,  # Bad Request
    'AuthenticationError': 401  # Unauthorized
}

class AuthenticationError(Exception):
    """Custom exception for authentication errors."""

def authenticate():
    """Validate authentication token.

    :header auth_token [str]: authentication token
    :returns user [User]: authenticated user's database object
    :raises AuthenticationError: if authentication fails
    """
    token = flask.request.headers.get('auth_token')
    if not token:
        raise AuthenticationError('missing auth token')

    # decode and verify token
    try:
        payload = jwt.decode(token, constants.SECRET_KEY, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AuthenticationError('expired')
    except jwt.DecodeError:
        raise AuthenticationError('invalid token format')
    if payload.get('ipa') != flask.request.remote_addr:
        raise AuthenticationError('mismatched ip address')

    # ensure user is not signed out
    if database.AuthTokenBlacklist.query.get(token):
        raise AuthenticationError('token signed out')

    # fetch user from token subject
    userId = payload.get('sub')
    user = database.User.query.get(userId)
    if not user:
        raise AuthenticationError('user does not exist')
    return user

def encrypt(password):
    """Encrypt a plain text password.

    :param password [str]: plain text password
    :returns [str]: SHA256-encrypted password
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def parse(name, type, optional=False):
    """Parse request parameter.

    :param name [str]: parameter name
    :param type [type]: type of variable to parse parameter into
    :param optional [bool]: if False, fail if unable to parse parameter
    :returns [any]: converted request parameter
    :raises ValueError: if unable to parse parameter
    """
    param = flask.request.form.get(name)
    if param:
        return type(param)
    elif not optional:
        raise ValueError(f'missing {name} parameter')
    return param

def route(app, url, method, func):
    """Create API route.

    Generates routes that direct requests to functions within the application.

    :param app [Flask]: Flask application object
    :param url [str]: url to route request from
    :param method [str]: http method type (GET, POST, etc.)
    :param func [function]: function to route request to
    """
    app.route(f'{constants.API_ROOT}/{url}',
              methods=[method],
              defaults={'func': func})(_call)

def tokenize(user):
    """
    Generate an authentication token.

    https://realpython.com/token-based-authentication-with-flask/

    :param user [User]: user database model to authenticate
    :returns [str]: auth token
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=constants.AUTH_TOKEN_LIFESPAN_SEC),  # expiration date
        'iat': datetime.datetime.utcnow(),  # time created
        'sub': user.id,  # subject
        'ipa': flask.request.remote_addr  # ip address
    }
    return jwt.encode(payload, constants.SECRET_KEY, algorithm='HS256')

def _call(func):
    """Call API function.

    Gracefully responds to requests that raise exceptions.

    :param func [function]: function to call
    :returns [tuple[dict, int]]: JSON response via helper functions
    """
    try:
        return _success(func())
    except Exception as error:
        return _failure(error)

def _failure(error):
    """Failed request response.

    Format:
    {
        "response": {
            "error": <error type>,
            "message": <error message>
        },
        "success": false
    }

    :param error [str]: description of error
    :returns [tuple[dict, int]]: JSON response in format (response, status code)
    """
    resp = constants.RESPONSE_TEMPLATE.copy()
    resp['success'] = False
    resp['response'] = {}
    errorType = type(error).__name__
    resp['response']['error'] = errorType
    resp['response']['message'] = str(error)
    return resp, _EXCEPTION_TO_HTTP_STATUS_CODE.get(errorType, 500)  # 500 Internal Server Error

def _success(response=None):
    """Successful request response.

    Format:
    {
        "response": <response>,
        "success": true
    }

    :param response [str]: request response
    :returns [tuple[dict, int]]: JSON response in format (response, status code)
    """
    resp = constants.RESPONSE_TEMPLATE.copy()
    if response is not None:
        resp['response'] = response
    return resp, 200  # 200 OK
