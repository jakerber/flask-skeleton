"""Application constants."""
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())  # load from .env

# API constants
API_ROOT = '/api/v1'
AUTH_TOKEN_LIFESPAN_SEC = int(os.environ['AUTH_TOKEN_LIFESPAN_SEC'])
FLASK_ENV = os.environ['FLASK_ENV']
RESPONSE_TEMPLATE = {'success': True, 'response': ''}
SECRET_KEY = os.environ['SECRET_KEY']

# Database constants
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_ECHO = os.environ['SQLALCHEMY_ECHO']
SQLALCHEMY_TRACK_MODIFICATIONS = bool(
    os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'])
