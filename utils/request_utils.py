"""API request utilities."""
import config
import datetime
import flask
import errors


def call(func):
    """Call API wrapper.

    Gracefully responds to requests that raise exceptions.

    :param func [function]: function to call
    :returns [tuple[dict, int]]: JSON response via helper functions
    """
    try:
        return _success(func())
    except Exception as error:
        return _failure(error)


def parse(name, format, optional=False):
    """Parse request parameter.

    :param name [str]: parameter name
    :param format [type]: type of variable to parse parameter into
    :param optional [bool]: if False, fail if unable to parse parameter
    :returns [any]: converted request parameter
    :raises MissingParameter: if parameter is missing from request body
    :raises UnprocessableRequest: if parameter is in invalid format
    """
    param = flask.request.form.get(name)
    if param:
        try:
            return format(param)
        except ValueError as error:
            raise errors.UnprocessableRequest(
                f"unable to parse '{param}' into {format.__name__}: "
                f'{str(error)}')
    elif not optional:
        raise errors.MissingParameter(f'missing {name} parameter')
    return param  # optional parameter is None


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
    :returns [tuple[dict, int]]: JSON response as (response, status code)
    """
    resp = config.RESPONSE_TEMPLATE.copy()
    resp['success'] = False
    resp['response'] = {}
    errorType = type(error).__name__
    resp['response']['error'] = errorType
    resp['response']['message'] = str(error)

    # Default status 500 Internal Server Error
    responseCode = 500
    if isinstance(error, errors.CustomException):
        responseCode = error.httpResponseCode
    return resp, responseCode


def _success(response=None):
    """Successful request response.

    Format:
    {
        "response": <response>,
        "success": true
    }

    :param response [str]: request response
    :returns [tuple[dict, int]]: JSON response as (response, status code)
    """
    resp = config.RESPONSE_TEMPLATE.copy()
    if response is not None:
        resp['response'] = response

    # Status 200 OK
    return resp, 200
