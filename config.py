import os

class Config:
    
    SECRET_KEY = os.environ.get('SECRETKEYF')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    