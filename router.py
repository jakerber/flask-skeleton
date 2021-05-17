"""API request router."""
import config
from api import admin_endpoints
from api import auth_endpoints
from api import stuff_endpoints
from api import user_endpoints
from utils import handler


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
    _createRoute(app, url='', method='GET', func=lambda: 'Bleep bloop')

    # Authentication endpoints
    _createRoute(app, url='auth', method='GET',
        func=auth_endpoints.signIn)
    _createRoute(app, url='auth', method='DELETE',
        func=auth_endpoints.signOut)
    _createRoute(app, url='auth', method='PUT',
        func=auth_endpoints.signUp)

    # User endpoints
    _createRoute(app, url='user', method='GET',
        func=user_endpoints.getUser)
    _createRoute(app, url='user', method='POST',
        func=user_endpoints.updateUser)
    _createRoute(app, url='user', method='DELETE',
        func=user_endpoints.deleteUser)

    # Stuff endpoints
    _createRoute(app, url='stuff', method='GET',
        func=stuff_endpoints.getStuff)
    _createRoute(app, url='stuff', method='PUT',
        func=stuff_endpoints.createStuff)
    _createRoute(app, url='stuff', method='POST',
        func=stuff_endpoints.updateStuff)
    _createRoute(app, url='stuff', method='DELETE',
        func=stuff_endpoints.deleteStuff)

    # Admin endpoints
    _createRoute(app, url='admin/user', method='GET',
        func=admin_endpoints.getUser)
    _createRoute(app, url='admin/users', method='GET',
        func=admin_endpoints.getAllUsers)
    _createRoute(app, url='admin/stuff', method='GET',
        func=admin_endpoints.getAllStuff)
    _createRoute(app, url='admin/tokens', method='GET',
        func=admin_endpoints.getBlacklistedTokens)
    _createRoute(app, url='admin/user',   method='DELETE',
        func=admin_endpoints.deleteUser)


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
              defaults={'func': func})(handler.call)
