"""Application constants."""
import os

# api constants
API_ROOT = '/api/v1'
AUTH_TOKEN_LIFESPAN_SEC = int(os.environ['AUTH_TOKEN_LIFESPAN_SEC'])
DEV_ENV = bool(os.environ['DEV_ENV'])
RESPONSE_TEMPLATE = {'success': True, 'response': ''}
SECRET_KEY = os.environ['SECRET_KEY']

# database constants
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_ECHO = os.environ['SQLALCHEMY_ECHO']
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'])
