"""Flask app runner."""
try:
    import config  # Safely initialize application config
except KeyError as error:
    raise RuntimeError(f'missing environment variable: {str(error)}')
import flask
import json
import router
from db import database

# Initialize Flask app
app = flask.Flask(__name__)

# Connect to database
SQLALCHEMY_TRACK_MODIFICATIONS = config.SQLALCHEMY_TRACK_MODIFICATIONS
SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI.replace(
    'postgres://',  # Heroku bug https://stackoverflow.com/q/62688256
    'postgresql://')
database.DB.init_app(app)

# Create tables if necessary
with app.app_context():
    database.DB.create_all()

# Set API request routes
router.route(app)


if __name__ == '__main__':
    app.run()
