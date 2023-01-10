import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
    ADMINS = ['asdf@gmail.com']
    LANGUAGES = ['en', 'uk']
    OPENSEARCH_URL = os.environ.get('OPENSEARCH_URL')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    POSTS_JSON_DIR = os.path.join('app', 'posts_json')

    # FLASK_ENV = 'development'
    # FLASK_APP = 'microblog'

