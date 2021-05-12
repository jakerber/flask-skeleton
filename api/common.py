"""Common API module."""
import constants
import datetime
import hashlib
import flask
import jwt

def encrypt(password):
    """Encrypt a plain text password.

    :param password [str]: plain text password
    :returns [str]: SHA256-encrypted password
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def endpoint(func):
    """Endpoint used for all API routes.

    Gracefully responds to requests that raise exceptions.

    :param func [function]: function to route request to
    :returns [tuple[dict, int]]: JSON response in format (response, status code)
    """
    try:
        return _success(func())
    except Exception as error:
        return _failure(error)

def decode(token):
    """Decode authentication token.

    https://realpython.com/token-based-authentication-with-flask/

    :param token [str]: auth token
    :returns [str]: decoded user identifier (phone number)
    """
    payload = jwt.decode(token, constants.SECRET_KEY)
    return payload['sub']

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
        'sub': user.phone  # subject
    }
    return jwt.encode(payload, constants.SECRET_KEY, algorithm='HS256')

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

    https://developer.mozilla.org/docs/Web/HTTP/Status

    :param error [str]: description of error
    :param statusCode [int]: HTTP failure status code
    :returns [tuple[dict, int]]: JSON response in format (response, status code)
    """
    resp = constants.RESPONSE_TEMPLATE.copy()
    resp['success'] = False
    resp['response'] = {}
    resp['response']['error'] = type(error).__name__
    resp['response']['message'] = str(error)
    return resp, 500  # 500 Internal Server Error
