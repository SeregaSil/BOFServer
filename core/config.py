import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

SECRET_KEY = os.environ.get('SECRET_KEY')
HASH_SALT = os.environ.get('HASH_SALT')
ALGORITHM = os.environ.get('ALGORITHM')

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

REDIS_USER = os.environ.get('REDIS_USER')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

ACCESS_TOKEN_ALIVE = int(os.environ.get('ACCESS_TOKEN_ALIVE'))
REFRESH_TOKEN_ALIVE = int(os.environ.get('REFRESH_TOKEN_ALIVE'))
