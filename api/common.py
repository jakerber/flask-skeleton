"""Common API functions."""
import constants
import hashlib
import flask

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
    param = flask.request.form.get(name, None)
    if param:
        try:
            return type(param)
        except ValueError as error:
            raise ValueError(f"invalid {param} parameter: {repr(error)}")
    elif not optional:
        raise ValueError(f"missing {name} parameter")
    return param

def success(response=None):
    """Successful request response.

    :param response [str]: request response
    :returns [tuple[dict, int]]: JSON response in format (response, status code)
    """
    resp = constants.RESPONSE_TEMPLATE.copy()
    if response:
        resp['response'] = response
    return resp, 200

def failure(error, statusCode=500):  # 500 Internal Server Error
    """Failed request response.

    https://developer.mozilla.org/docs/Web/HTTP/Status

    :param error [str]: description of error
    :param statusCode [int]: HTTP failure status code
    :returns [tuple[dict, int]]: JSON response in format (response, status code)
    """
    resp = constants.RESPONSE_TEMPLATE.copy()
    resp['success'] = False
    resp['response'] = error
    return resp, statusCode
