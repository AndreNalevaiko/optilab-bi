import os

APP_NAME = 'optilab-bi-api'
APP_VERSION = '1.0.0'
API_VERSION = 'v1'

SECRET_KEY = os.environ['SECRET_KEY']

DATABASE_URL = os.environ['DATABASE_MYSQL']
DATABASE_METRICS = os.environ['DATABASE_METRICS']
DATABASE_FIREBIRD = os.environ['DATABASE_FIREBIRD']

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 10
SQLALCHEMY_POOL_RECYCLE = 60 * 5
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_MYSQL']
SQLALCHEMY_ECHO = False