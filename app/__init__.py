from flask import Flask, request
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l


application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
mail = Mail(application)
bootstrap = Bootstrap(application)


login = LoginManager(application)
from app import routes, models, errors
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')

moment = Moment(application)
babel = Babel(application)

if not application.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)

    application.logger.setLevel(logging.INFO)
    application.logger.info('Microblog startup')

@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(application.config['LANGUAGES'])
    return 'uk'



