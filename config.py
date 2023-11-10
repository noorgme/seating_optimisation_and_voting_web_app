import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:password@localhost:3306/votingdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
