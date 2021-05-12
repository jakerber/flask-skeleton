"""Flask app runner."""
try:
    import constants  # Safely initialize application constants
except KeyError as error:
    raise RuntimeError(f'missing environment variable: {str(error)}')
import database
import flask
import json
from api import auth
from api import common
from api import stuff
from api import user

# Initialize Flask app
app = flask.Flask(__name__)

# Connect to database
SQLALCHEMY_TRACK_MODIFICATIONS = constants.SQLALCHEMY_TRACK_MODIFICATIONS
SQLALCHEMY_DATABASE_URI = constants.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI.replace(
    'postgres://',  # Heroku bug https://stackoverflow.com/q/62688256
    'postgresql://')
database.DB.init_app(app)

# Create tables if necessary
with app.app_context():
    database.DB.create_all()

"""
API router.
"""


# Application root
@app.route('/')
def root():
    """Returns HTML link to API root."""
    return f'<a href="{constants.API_ROOT}">{constants.API_ROOT}</a>', 200


# API root
common.route(app, url='', method='GET', func=lambda: 'Hello, world!')

# Authentication operations
common.route(app, url='auth', method='GET',    func=auth.signIn)
common.route(app, url='auth', method='DELETE', func=auth.signOut)
common.route(app, url='auth', method='PUT',    func=auth.signUp)

# User operations
common.route(app, url='user', method='GET',    func=user.getUser)
common.route(app, url='user', method='POST',   func=user.updateUser)
common.route(app, url='user', method='DELETE', func=user.deleteUser)

# Stuff operations
common.route(app, url='stuff', method='GET',    func=stuff.getStuff)
common.route(app, url='stuff', method='PUT',    func=stuff.createStuff)
common.route(app, url='stuff', method='POST',   func=stuff.updateStuff)
common.route(app, url='stuff', method='DELETE', func=stuff.deleteStuff)

# Test endpoints
if constants.FLASK_ENV == 'development':
    common.route(app, url='users',  method='GET', func=user.getAllUsers)
    common.route(app, url='stuffs', method='GET', func=stuff.getAllStuff)
    common.route(app, url='tokens', method='GET', func=auth.getBlacklistTokens)


if __name__ == '__main__':
    app.run()
