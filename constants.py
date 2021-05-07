"""Application constants."""
import os

# api constants
API_ROOT = '/api/v1'
DEBUG = bool(os.getenv('DEBUG'))
RESPONSE_TEMPLATE = {'success': True, 'response': ''}

# database constants
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO')
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
