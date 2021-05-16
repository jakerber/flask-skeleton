"""API request router."""
import config
from api import admin_api
from api import auth_api
from api import stuff_api
from api import user_api
from utils import request_utils


def route(app):
    """Initialize router for API requests.

    :param app [Flask]: Flask app instance.
    """
    # Application root
    @app.route('/')
    def root():
        """Returns HTML link to API root."""
        return f'<a href="{config.API_ROOT}">{config.API_ROOT}</a>'

    # API root
    _createRoute(app, url='', method='GET', func=lambda: 'Hello, world!')

    # Authentication operations
    _createRoute(app, url='auth', method='GET',    func=auth_api.signIn)
    _createRoute(app, url='auth', method='DELETE', func=auth_api.signOut)
    _createRoute(app, url='auth', method='PUT',    func=auth_api.signUp)

    # User operations
    _createRoute(app, url='user', method='GET',    func=user_api.getUser)
    _createRoute(app, url='user', method='POST',   func=user_api.updateUser)
    _createRoute(app, url='user', method='DELETE', func=user_api.deleteUser)

    # Stuff operations
    _createRoute(app, url='stuff', method='GET',    func=stuff_api.getStuff)
    _createRoute(app, url='stuff', method='PUT',    func=stuff_api.createStuff)
    _createRoute(app, url='stuff', method='POST',   func=stuff_api.updateStuff)
    _createRoute(app, url='stuff', method='DELETE', func=stuff_api.deleteStuff)

    # Admin endpoints
    _createRoute(app, url='admin/user',   method='GET',
        func=admin_api.getUser)
    _createRoute(app, url='admin/users',  method='GET',
        func=admin_api.getAllUsers)
    _createRoute(app, url='admin/stuff',  method='GET',
        func=admin_api.getAllStuff)
    _createRoute(app, url='admin/tokens', method='GET',
        func=admin_api.getBlacklistedTokens)
    _createRoute(app, url='admin/user',   method='DELETE',
        func=admin_api.deleteUser)


def _createRoute(app, url, method, func):
    """Create API route.

    Generates routes that direct requests to functions within the application.

    :param app [Flask]: Flask application object
    :param url [str]: url to route request from
    :param method [str]: http method type (GET, POST, etc.)
    :param func [function]: function to route request to
    """
    app.route(f'{config.API_ROOT}/{url}',
              methods=[method],
              defaults={'func': func})(request_utils.call)
