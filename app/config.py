from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'StandardKey'
    ALCHEMICAL_DATABASE_URL = environ.get('DATABASE_URL') or 'sqlite:///app.db'
    CLIENT_ID = environ.get('CLIENT_ID')
    CLIENT_SECRET = environ.get('CLIENT_SECRET')
    AUTH_URL = environ.get('AUTH_URL')
    TOKEN_URL = environ.get('TOKEN_URL')
    USERINFO_URL = environ.get('USERINFO_URL')
    LOGOUT_URL = environ.get('LOGOUT_URL')
    REDIRECT_URI = environ.get('REDIRECT_URI')
