"""Backend server."""
try:
    import constants  # safely initialize application constants
except KeyError as error:
    raise RuntimeError(f'missing environment variable: {str(error)}')
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

# api root
@app.route(f'{constants.API_ROOT}', methods=['GET'])
def root():
    return 'Hello, world!', 200

# authentication operations
common.route(app, url='auth', method='GET',    func=auth.signIn, auth=False)
common.route(app, url='auth', method='DELETE', func=auth.signOut)

# user operations
common.route(app, url='user', method='PUT',    func=user.createUser, auth=False)
common.route(app, url='user', method='POST',   func=user.modifyUserName)
common.route(app, url='user', method='DELETE', func=user.deleteUser)

# item operations
common.route(app, url='item', method='PUT',    func=item.createItem)
common.route(app, url='item', method='POST',   func=item.modifyItemValue)
common.route(app, url='item', method='DELETE', func=item.deleteItem)

# test endpoints
if constants.DEV_ENV:
    common.route(app, url='user', method='GET', func=user.getUsers, auth=False)
    common.route(app, url='item', method='GET', func=item.getItems, auth=False)

"""
Flask app runner.
"""

if __name__ == '__main__':
    app.run(debug=constants.DEV_ENV)
