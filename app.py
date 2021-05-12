"""Backend server."""
import constants
import database
import flask
import json
from api import auth
from api import common
from api import item
from api import user

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

# api gateway
gateway = common.endpoint

# api root
@app.route(f'{constants.API_ROOT}', methods=['GET'])
def root():
    return 'Hello, world!', 200

# authentication operations
app.route(f'{constants.API_ROOT}/auth', methods=['GET'], defaults={'func': auth.signIn})(gateway)
app.route(f'{constants.API_ROOT}/auth', methods=['DELETE'], defaults={'func': auth.signOut})(gateway)

# user operations
app.route(f'{constants.API_ROOT}/user', methods=['GET'], defaults={'func': user.getUsers})(gateway)
app.route(f'{constants.API_ROOT}/user', methods=['PUT'], defaults={'func': user.createUser})(gateway)
app.route(f'{constants.API_ROOT}/user', methods=['POST'], defaults={'func': user.modifyUserName})(gateway)
app.route(f'{constants.API_ROOT}/user', methods=['DELETE'], defaults={'func': user.deleteUser})(gateway)

# item operations
app.route(f'{constants.API_ROOT}/item', methods=['GET'], defaults={'func': item.getItems})(gateway)
app.route(f'{constants.API_ROOT}/item', methods=['PUT'], defaults={'func': item.createItem})(gateway)
app.route(f'{constants.API_ROOT}/item', methods=['POST'], defaults={'func': item.modifyItemValue})(gateway)
app.route(f'{constants.API_ROOT}/item', methods=['DELETE'], defaults={'func': item.deleteItem})(gateway)

"""
Flask app runner.
"""

if __name__ == '__main__':
    app.run(debug=constants.DEBUG)
