"""Common API module."""
import constants
import hashlib
import flask

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

def encrypt(password):
    """Encrypt a plain text password.

    :param password [str]: plain text password
    :returns [str]: SHA256-encrypted password
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

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
    if response:
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
