"""Backend server."""
import constants
import flask
from api import auth
from api import item
from api import user
from db import database

# initialize Flask app
app = flask.Flask(__name__)

# initialize SQLAlchemy database
SQLALCHEMY_TRACK_MODIFICATIONS = constants.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = constants.SQLALCHEMY_DATABASE_URI
database.DB.init_app(app)

# create tables if necessary
with app.app_context():
    database.DB.create_all()

"""
API router.
"""

# api root
@app.route(f'{constants.API_ROOT}', methods=['GET'])
def root():
    return 'Hello, world!', 200

# authentication operations
app.route(f'{constants.API_ROOT}/auth', methods=['GET'])(auth.signIn)
app.route(f'{constants.API_ROOT}/auth', methods=['DELETE'])(auth.signOut)

# user operations
app.route(f'{constants.API_ROOT}/user', methods=['GET'])(user.getUsers)
app.route(f'{constants.API_ROOT}/user', methods=['PUT'])(user.createUser)
app.route(f'{constants.API_ROOT}/user', methods=['POST'])(user.modifyUser)
app.route(f'{constants.API_ROOT}/user', methods=['DELETE'])(user.deleteUser)

# item operations
app.route(f'{constants.API_ROOT}/item', methods=['GET'])(item.getItems)
app.route(f'{constants.API_ROOT}/item', methods=['PUT'])(item.createItem)
app.route(f'{constants.API_ROOT}/item', methods=['POST'])(item.modifyItem)
app.route(f'{constants.API_ROOT}/item', methods=['DELETE'])(item.deleteItem)

"""
Flask app runner.
"""

if __name__ == '__main__':
    app.run(debug=constants.DEBUG)
